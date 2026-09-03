import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carga de variables de entorno
load_dotenv()

# --- CONFIGURACIÓN DE PÁGINA STREAMLIT ---
st.set_page_config(
    page_title="NIA | Asistente Virtual Oficial ISTCGE",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- BASE DE CONOCIMIENTO INSTITUCIONAL Y COMERCIAL (ISTCGE / ASCEND) ---
KNOWLEDGE_CONTEXT = """
1. IDENTIDAD INSTITUCIONAL Y DATOS GENERALES:
- Nombre oficial: Instituto Superior Tecnológico CGE (ISTCGE).
- Sitio Web Oficial: https://web.istcge.edu.ec/
- Ecosistema Educativo: ASCEND (Formación Superior 100% en línea).
- Títulos Otorgados: Títulos Oficiales de Tercer Nivel Tecnológico avalados por el Consejo de Educación Superior (CES) del Ecuador.
- Modalidad: 100% en línea (virtual, flexible y asincrónica, compatible con trabajo y familia).
- Slogan y Filosofía: «No solo estudies una carrera. Construye tu siguiente nivel».

2. PROGRAMAS ACADÉMICOS Y CARRERAS:
A) TECNOLOGÍA SUPERIOR EN DESARROLLO DE SOFTWARE:
- Título Oficial: Tecnólogo/a Superior en Desarrollo de Software (Tercer Nivel).
- Lema: «Convierte problemas reales en soluciones digitales».
- Competencias: Programación web y móvil, bases de datos, arquitectura de software y aplicaciones con Inteligencia Artificial.
- Dirigido a: Personas que inician desde cero, programadores empíricos y técnicos.

B) TECNOLOGÍA SUPERIOR EN VENTAS DIGITALES:
- Título Oficial: Tecnólogo/a Superior en Ventas Digitales (Tercer Nivel).
- Lema: «Convierte ideas, productos y oportunidades en resultados».
- Competencias: Estrategias omnicanal, embudos de conversión (funnels), marketing digital, CRM y comercio electrónico (e-commerce).
- Dirigido a: Emprendedores, vendedores, comerciales y bachilleres.

3. RUTAS DE INGRESO Y ADMISIÓN:
- Ruta «Empieza Desde Cero»: Para quienes no tienen experiencia previa. Aprendizaje práctico desde las bases con IA y tutores.
- Ruta «Homologación y Validación de Experiencia Laboral»: Permite convalidar materias aprobadas en universidades/institutos o certificar años de experiencia laboral para titularse en menor tiempo.
- Ruta «ISTCGE para Empresas»: Planes corporativos de titulación y capacitación para equipos de trabajo.

4. TEST VOCACIONAL ASCEND (GRATUITO):
- Cuestionario de orientación para quienes dudan qué carrera elegir.
- Identifica 4 perfiles: Conector Comercial (Ventas), Constructor Digital (Software), Híbrido y Explorador.

5. VENTAJAS DIFERENCIALES:
- Inteligencia Artificial aplicada en todas las materias.
- Clases prácticas basadas en proyectos reales (no pura teoría).
- Mentorías en vivo, webinars con expertos del sector y acompañamiento humano continuo.
"""

SALUDOS_GENERICOS = ["hola", "buenos dias", "buenas tardes", "buenas noches", "saludos", "hola!", "holaa", "buenas", "que tal", "hola nia"]

def es_saludo_generico(text):
    clean = text.lower().strip().replace(".", "").replace("!", "").replace("¿", "").replace("?", "")
    return clean in SALUDOS_GENERICOS

# --- OBTENCIÓN RESILIENTE DEL CLIENTE IA DE GEMINI ---
def get_gemini_response(prompt_text, history_messages):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]

    if not api_key:
        return "⚠️ Debes configurar la clave 'GEMINI_API_KEY' en los Secrets de Streamlit."

    genai.configure(api_key=api_key)

    # Prompt del sistema con enfoque comercial ISTCGE
    system_instruction = f"""
Eres NIA, la asesora virtual oficial y comercial del Instituto Superior Tecnológico CGE (ISTCGE) y su plataforma educativa ASCEND.
Sitio web oficial: https://web.istcge.edu.ec/

OBJETIVO:
Guiar, informar, asesorar y motivar a prospectos, estudiantes y empresas interesadas en titularse con carreras oficiales de Tercer Nivel 100% en línea (Desarrollo de Software y Ventas Digitales), convalidación de experiencia laboral y admisiones.

NORMAS DE ATENCIÓN:
1. Habla SIEMPRE en ESPAÑOL con tono profesional, cálido, comercial, dinámico y muy claro.
2. Utiliza negritas, listas con viñetas y emojis institucionales (🎓, 💻, 📈, 🚀) para que el mensaje sea muy visual y atractivo.
3. Basa tus respuestas en la INFORMACIÓN INSTITUCIONAL de ISTCGE.
4. Concluye siempre con un llamado a la acción comercial o pregunta amable invitando al usuario a matricularse, hacer el test vocacional o solicitar contacto directo por WhatsApp.

INFORMACIÓN INSTITUCIONAL:
{KNOWLEDGE_CONTEXT}
"""

    # Modelos a probar en orden de compatibilidad
    candidate_models = [
        "gemini-flash-latest",
        "gemini-1.5-flash-latest",
        "gemini-pro",
        "gemini-1.5-flash-8b",
        "gemini-1.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-pro-latest"
    ]

    last_error = None
    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            # Formatear historial
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt_text)
            if response and response.text:
                return response.text
        except Exception as e:
            # Si el modelo no acepta system_instruction en el constructor, intentarlo combinado
            try:
                model_alt = genai.GenerativeModel(model_name=model_name)
                full_prompt = f"{system_instruction}\n\n[CONSULTA DEL POSTULANTE]:\n{prompt_text}"
                response = model_alt.generate_content(full_prompt)
                if response and response.text:
                    return response.text
            except Exception as ex:
                last_error = ex
                continue

    return f"Disculpa, ocurrió un inconveniente con el servicio de IA: {str(last_error)}"

# --- DISEÑO VISUAL CORPORATIVO Y COMERCIAL ISTCGE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Variables de Color ISTCGE */
    :root {
        --cge-blue: #002C5A;
        --cge-navy: #0F172A;
        --cge-cyan: #009CDE;
        --cge-yellow: #FDC901;
        --cge-bg: #070D18;
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #0d223f 0%, #050a14 100%) !important;
        font-family: 'Inter', sans-serif !important;
        color: #F8FAFC !important;
    }

    /* Ocultar elementos innecesarios */
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Header Comercial CGE */
    .cge-header-card {
        background: linear-gradient(135deg, rgba(0, 44, 90, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(0, 156, 222, 0.3);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
    }

    .cge-title-box h1 {
        color: #FFFFFF !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }

    .cge-title-box p {
        color: #94A3B8 !important;
        font-size: 0.9rem !important;
        margin: 4px 0 0 0 !important;
    }

    .cge-badge-gold {
        background: linear-gradient(135deg, #FDC901, #D97706);
        color: #000000 !important;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 4px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .cge-badge-status {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
    }

    /* Tarjetas de Beneficios Comerciales */
    .cge-highlights-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }

    .cge-highlight-chip {
        background: rgba(0, 44, 90, 0.4);
        border: 1px solid rgba(0, 156, 222, 0.2);
        color: #E2E8F0 !important;
        padding: 8px 14px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Burbujas de Chat */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px);
    }

    /* Input */
    .stChatInputContainer {
        background-color: #0b1320 !important;
        border: 1px solid rgba(0, 156, 222, 0.4) !important;
        border-radius: 14px !important;
    }

    /* CTA WhatsApp Bar */
    .whatsapp-cta {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white !important;
        text-decoration: none;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: transform 0.2s;
    }
    .whatsapp-cta:hover {
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER COMERCIAL ISTCGE ---
st.markdown("""
<div class="cge-header-card">
    <div class="cge-title-box">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <h1>🎓 NIA • Asesora Oficial ISTCGE</h1>
            <span class="cge-badge-gold">Oficial CES</span>
        </div>
        <p>Instituto Superior Tecnológico CGE • Plataforma Formativa ASCEND (100% Online)</p>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <span class="cge-badge-status">
            <span class="status-dot"></span>
            Asesora en Línea
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- CHIPS INFORMATIVOS COMERCIALES ---
st.markdown("""
<div class="cge-highlights-container">
    <div class="cge-highlight-chip">💻 Tecnología en Desarrollo de Software</div>
    <div class="cge-highlight-chip">📈 Tecnología en Ventas Digitales</div>
    <div class="cge-highlight-chip">📜 Convalidación de Experiencia Laboral</div>
    <div class="cge-highlight-chip">🧭 Test Vocacional Gratuito</div>
    <div class="cge-highlight-chip">⚡ 100% Virtual Asincrónico</div>
</div>
""", unsafe_allow_html=True)

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! 👋 Soy **NIA**, asesora virtual del **Instituto Superior Tecnológico CGE (ISTCGE)** y nuestro ecosistema **ASCEND**.\n\nTe ayudo con todo sobre nuestras **carreras oficiales de tercer nivel 100% online** (Desarrollo de Software y Ventas Digitales), homologación de materias, validación de experiencia laboral y admisiones.\n\n¿En qué carrera o trámite estás interesado hoy?"
        }
    ]

# Renderizar mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Capturar mensaje del usuario
if prompt := st.chat_input("Escribe tu consulta sobre carreras, costos, convalidación o matrícula..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if es_saludo_generico(prompt):
            reply = "¡Hola! Qué gusto saludarte. 😊 En **ISTCGE** te ofrecemos carreras tecnológicas oficiales de tercer nivel 100% en línea:\n\n* 💻 **Tecnología Superior en Desarrollo de Software**\n* 📈 **Tecnología Superior en Ventas Digitales**\n* 📜 **Homologación y Validación de Experiencia Laboral**\n\n¿De cuál de ellas te gustaría recibir más información o costos?"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            with st.spinner("NIA está consultando la información oficial..."):
                response_text = get_gemini_response(prompt, st.session_state.messages)
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
