import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carga de variables de entorno
load_dotenv()

# --- CONFIGURACIÓN DE PÁGINA STREAMLIT ---
st.set_page_config(
    page_title="NIA | Asesora Comercial ISTCGE",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- BASE DE CONOCIMIENTO COMERCIAL ISTCGE / ASCEND ---
KNOWLEDGE_CONTEXT = """
1. IDENTIDAD INSTITUCIONAL Y PROPUESTA DE VALOR:
- Nombre oficial: Instituto Superior Tecnológico CGE (ISTCGE) - Ecosistema Formativo ASCEND.
- Sitio Web Oficial: https://web.istcge.edu.ec/
- Títulos: Títulos Oficiales de Tercer Nivel Tecnológico avalados por el Consejo de Educación Superior (CES) del Ecuador (registrados en SENESCYT).
- Modalidad: 100% en línea (virtual, asincrónica y flexible, ideal para quienes trabajan o tienen responsabilidades familiares).
- Slogan: «No solo estudies una carrera. Construye tu siguiente nivel».

2. OFERTA DE CARRERAS:
A) TECNOLOGÍA SUPERIOR EN DESARROLLO DE SOFTWARE:
- Título Oficial de Tercer Nivel Tecnológico.
- Beneficios: Aprende programación desde cero, desarrollo web y móvil, bases de datos e Inteligencia Artificial aplicada.
- Dirigido a: Bachilleres, técnicos, autodidactas y profesionales que buscan reconversión laboral hacia tecnología.

B) TECNOLOGÍA SUPERIOR EN VENTAS DIGITALES:
- Título Oficial de Tercer Nivel Tecnológico.
- Beneficios: Estrategias comerciales omnicanal, embudos de venta (funnels), marketing digital, e-commerce y CRM.
- Dirigido a: Emprendedores, vendedores tradicionales, bachilleres y equipos comerciales.

3. RUTAS DE INGRESO:
- «Empieza Desde Cero»: Formación completa paso a paso con acompañamiento docente e IA.
- «Homologación y Validación de Experiencia Laboral»: Convalida materias aprobadas en universidades o reconoce tu experiencia laboral práctica para titularte en menor tiempo.
- «ISTCGE para Empresas»: Planes corporativos de capacitación y titulación para equipos de trabajo.

4. TEST VOCACIONAL ASCEND (GRATUITO):
- Cuestionario rápido para orientar a postulantes indecisos e identificar su afinidad (Ventas Digitales, Desarrollo de Software, Híbrido o Explorador).

5. MANEJO DE PREGUNTAS Y OBJECIONES:
- Flexibilidad: Plataforma disponible 24/7 para estudiar al propio ritmo.
- Experiencia previa: No se requiere conocimiento previo en programación ni ventas.
- Validez oficial: Títulos de 3er nivel registrados legalmente en Ecuador.
- Contacto y Matrícula: Se invita al usuario a iniciar su inscripción o solicitar asesoría personalizada por WhatsApp.
"""

SALUDOS_GENERICOS = ["hola", "buenos dias", "buenas tardes", "buenas noches", "saludos", "hola!", "holaa", "buenas", "que tal", "hola nia", "info", "informacion", "precio", "costo"]

def es_saludo_generico(text):
    clean = text.lower().strip().replace(".", "").replace("!", "").replace("¿", "").replace("?", "")
    return clean in SALUDOS_GENERICOS

# --- CLIENTE RESILIENTE GEMINI ---
def get_gemini_response(prompt_text, history_messages):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]

    if not api_key:
        return "⚠️ Por favor configura tu clave 'GEMINI_API_KEY' en los Secrets de Streamlit."

    genai.configure(api_key=api_key)

    system_instruction = f"""
Eres NIA, la Asesora Comercial de Admisiones y Ventas del Instituto Superior Tecnológico CGE (ISTCGE) y su plataforma ASCEND.
Sitio web oficial: https://web.istcge.edu.ec/

TU ROL ES 100% COMERCIAL Y DE ASESORÍA DE VENTAS:
- No eres tutora ni docente académica. Eres una asesora de admisiones amable, profesional, ejecutiva y enfocada en orientar, persuadir y captar estudiantes para ISTCGE.
- Tu objetivo es presentar las ventajas de nuestras carreras oficiales de tercer nivel 100% en línea (Desarrollo de Software y Ventas Digitales), destacar la homologación de experiencia laboral y guiar al usuario hacia la matrícula o el contacto por WhatsApp con un asesor.

PAUTAS DE RESPUESTA:
1. Responde SIEMPRE en ESPAÑOL, con tono cálido, profesional, claro y vendedor.
2. Usa negritas para destacar ideas principales y listas ordenadas o con viñetas para facilitar la lectura.
3. Respuestas concisas, bien estructuradas y directas al grano.
4. Concluye siempre con una pregunta amable de cierre comercial o invitando a dar el siguiente paso (ej: evaluar experiencia para homologación, hacer el test vocacional o solicitar contacto por WhatsApp).

INFORMACIÓN INSTITUCIONAL Y COMERCIAL:
{KNOWLEDGE_CONTEXT}
"""

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
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt_text)
            if response and response.text:
                return response.text
        except Exception as e:
            try:
                model_alt = genai.GenerativeModel(model_name=model_name)
                full_prompt = f"{system_instruction}\n\n[CONSULTA DEL PROSPECTO]:\n{prompt_text}"
                response = model_alt.generate_content(full_prompt)
                if response and response.text:
                    return response.text
            except Exception as ex:
                last_error = ex
                continue

    return f"Disculpa, ocurrió un inconveniente con el servicio de IA: {str(last_error)}"

# --- ESTILOS VISUALES LIMPIOS, MINIMALISTAS Y ELEGANTES (ESTILO SOLICITADO) ---
st.markdown("""
    <style>
    /* Estilos base limpios y profesionales */
    .stApp {
        background-color: #f9fafb !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
        color: #1f2937 !important;
    }

    /* Ocultar barra superior y footer */
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Tarjeta principal estilo solicitado */
    .cge-card-header {
        max-width: 680px;
        margin: 0 auto 16px auto;
        padding: 16px 20px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .cge-header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .cge-avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background-color: #002c5a;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 0.5px;
    }

    .cge-header-titles h1 {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #111827 !important;
        margin: 0 !important;
        line-height: 1.2;
    }

    .cge-header-titles p {
        color: rgb(107, 114, 128) !important;
        font-size: 13px !important;
        margin: 2px 0 0 0 !important;
    }

    .cge-badge-status {
        background-color: #ecfdf5;
        color: #059669;
        border: 1px solid #a7f3d0;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #10b981;
        border-radius: 50%;
    }

    /* Píldoras de Carreras */
    .cge-tags-container {
        max-width: 680px;
        margin: 0 auto 16px auto;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .cge-tag {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        color: #374151 !important;
        font-size: 12.5px;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 500;
    }

    /* Mensajes de Chat limpios */
    .stChatMessage {
        max-width: 680px !important;
        margin: 0 auto 10px auto !important;
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    }

    /* Textos en el chat */
    .stChatMessage p, .stChatMessage li, .stChatMessage span {
        color: #1f2937 !important;
        font-size: 14.5px !important;
        line-height: 1.55 !important;
    }

    .stChatMessage strong {
        color: #002c5a !important;
        font-weight: 600 !important;
    }

    /* Input del chat */
    .stChatInputContainer {
        max-width: 680px !important;
        margin: 0 auto !important;
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO MINIMALISTA ESTILO SOLICITADO ---
st.markdown("""
<div class="cge-card-header">
    <div class="cge-header-left">
        <div class="cge-avatar">CGE</div>
        <div class="cge-header-titles">
            <h1>NIA • Asesora Comercial ISTCGE</h1>
            <p>Instituto Superior Tecnológico CGE • Admisiones 100% Online</p>
        </div>
    </div>
    <span class="cge-badge-status">
        <span class="status-dot"></span>
        En línea
    </span>
</div>
""", unsafe_allow_html=True)

# --- PÍLDORAS INFORMATIVAS ---
st.markdown("""
<div class="cge-tags-container">
    <div class="cge-tag">💻 Tec. en Desarrollo de Software</div>
    <div class="cge-tag">📈 Tec. en Ventas Digitales</div>
    <div class="cge-tag">⚡ Homologación de Experiencia</div>
    <div class="cge-tag">🧭 Test Vocacional Gratuito</div>
    <div class="cge-tag">🎓 Títulos Oficiales CES</div>
</div>
""", unsafe_allow_html=True)

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Te saluda **NIA**, asesora comercial de admisiones del **Instituto Superior Tecnológico CGE (ISTCGE)**.\n\nTe ayudo a elegir tu carrera de tercer nivel tecnológico 100% en línea:\n\n* 💻 **Tecnología Superior en Desarrollo de Software**\n* 📈 **Tecnología Superior en Ventas Digitales**\n* ⚡ **Homologación de Experiencia Laboral** *(titulación acelerada)*\n* 🧭 **Test Vocacional Gratuito**\n\n¿En cuál de nuestras opciones te gustaría recibir información sobre requisitos, plan de estudios o facilidades de pago?"
        }
    ]

# Renderizar mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Capturar interacción del usuario
if prompt := st.chat_input("Escribe tu consulta sobre carreras, costos o matrícula..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if es_saludo_generico(prompt):
            reply = "¡Hola! Qué gusto saludarte. En **ISTCGE** contamos con convocatorias abiertas para nuestras carreras oficiales de tercer nivel 100% en línea:\n\n1. 💻 **Tecnología Superior en Desarrollo de Software**\n2. 📈 **Tecnología Superior en Ventas Digitales**\n3. ⚡ **Homologación y Validación de Experiencia Laboral**\n\n¿De cuál de ellas deseas conocer los detalles o beneficios de matrícula?"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            with st.spinner("NIA está procesando tu consulta..."):
                response_text = get_gemini_response(prompt, st.session_state.messages)
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
