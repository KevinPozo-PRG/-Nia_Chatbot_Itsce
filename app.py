import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carga de variables de entorno
load_dotenv()

# --- CONFIGURACIÓN DE PÁGINA STREAMLIT ---
st.set_page_config(
    page_title="NIA | Asesora Comercial de Admisiones ISTCGE",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- BASE DE CONOCIMIENTO COMERCIAL Y DE VENTAS ISTCGE / ASCEND ---
KNOWLEDGE_CONTEXT = """
1. IDENTIDAD INSTITUCIONAL Y PROPUESTA DE VALOR COMERCIAL:
- Nombre oficial: Instituto Superior Tecnológico CGE (ISTCGE) - Ecosistema Formativo ASCEND.
- Sitio Web Oficial: https://web.istcge.edu.ec/
- Títulos: Títulos Oficiales de Tercer Nivel Tecnológico avalados por el Consejo de Educación Superior (CES) del Ecuador (registrados en SENESCYT).
- Modalidad: 100% en línea (virtual, asincrónica y flexible, ideal para personas que trabajan, cuidan familia o emprenden).
- Promesa de Venta: «No solo estudies una carrera. Construye tu siguiente nivel. Integramos aprendizaje práctico, inteligencia artificial y mentorías para que avances sin detener tu vida».

2. OFERTA DE CARRERAS (PRODUCTOS DESTACADOS):
A) TECNOLOGÍA SUPERIOR EN DESARROLLO DE SOFTWARE:
- Propuesta comercial: «Convierte problemas reales en soluciones digitales y accede a los empleos mejor pagados del sector tecnológico».
- Beneficios clave: Aprende programación desde cero, desarrollo web, apps móviles, inteligencia artificial y bases de datos con proyectos reales para armar tu portafolio desde el primer día.
- Para quién es: Bachilleres, profesionales que buscan reconversión laboral, autodidactas o programadores empíricos que necesitan el título oficial de tercer nivel para ascensos y licitaciones.

B) TECNOLOGÍA SUPERIOR EN VENTAS DIGITALES:
- Propuesta comercial: «Convierte ideas, productos y oportunidades en ventas millonarias».
- Beneficios clave: Estrategias omnicanal, embudos de venta (funnels), marketing digital, e-commerce, automatizaciones con IA y cierre de negocios modernos.
- Para quién es: Emprendedores que quieren escalar su negocio, vendedores tradicionales que quieren ganar más comisiones por internet y bachilleres con visión comercial.

3. RUTAS DE INGRESO Y BENEFICIOS EXCLUSIVOS:
- Ruta «Empieza Desde Cero»: Aprende desde las bases teóricas y prácticas, con acompañamiento personalizado y herramientas de IA.
- Ruta «Homologación y Validación de Experiencia Laboral»: ¡No empieces de cero! Si ya trabajaste en el área o tienes materias aprobadas en otra universidad o instituto, evaluamos tu experiencia y te convalidamos asignaturas para que te titules en TIEMPO RÉCORD.
- Ruta «ISTCGE para Empresas (B2B)»: Formación corporativa a medida para capacitar y titular equipos de trabajo con bonificaciones y planes corporativos.

4. HERRAMIENTA DE CONVERSIÓN - TEST VOCACIONAL GRATUITO:
- Si el prospecto tiene dudas de qué estudiar, ofrécele hacer el Test Vocacional ASCEND Gratuito para identificar su perfil: Conector Comercial (Ventas), Constructor Digital (Software), Híbrido o Explorador.

5. MANEJO DE OBJECIONES COMERCIALES:
- "No tengo tiempo": Nuestro modelo es 100% asincrónico y flexible; estudias a tu propio ritmo en los horarios que tú elijas.
- "No sé nada de programación o ventas": Nuestro programa empieza desde cero con tutores que te guían paso a paso.
- "¿Es título oficial?": Sí, título oficial de Tercer Nivel Tecnológico reconocido por el CES en Ecuador.
- "Ya tengo años trabajando": Puedes aplicar a la Validación de Experiencia Laboral y titularte mucho más rápido.

6. LLAMADOS A LA ACCIÓN (CTAs):
- Invita siempre al prospecto a: 1. Iniciar su proceso de matrícula, 2. Solicitar una llamada/chat de WhatsApp con un asesor comercial oficial, 3. Realizar el Test Vocacional o 4. Evaluar su experiencia laboral para homologación.
"""

SALUDOS_GENERICOS = ["hola", "buenos dias", "buenas tardes", "buenas noches", "saludos", "hola!", "holaa", "buenas", "que tal", "hola nia", "info", "informacion", "precio", "costo"]

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

    # Prompt del sistema con mentalidad 100% de Ventas Consultivas y Cierre Comercial
    system_instruction = f"""
Eres NIA, la Asesora Comercial de Admisiones y Ventas del Instituto Superior Tecnológico CGE (ISTCGE) y su plataforma educativa ASCEND.
Sitio web oficial: https://web.istcge.edu.ec/

TU ROL ES COMERCIAL Y DE VENTAS:
- NO eres una profesora ni tutora académica. Eres una EJECUTIVA COMERCIAL de alto nivel, experta en persuadir, asesorar, entusiasmar y captar estudiantes para ISTCGE.
- Tu misión principal es vender las carreras tecnológicas oficiales de tercer nivel (Desarrollo de Software y Ventas Digitales), promocionar los beneficios de homologar la experiencia laboral y conseguir que el usuario se matricule o contacte con un asesor de admisiones.

PAUTAS DE VENTAS Y ESTILO:
1. Enfoque en Beneficios y Retorno de Inversión: Habla de mejores salarios, ascensos laborales, título oficial de tercer nivel reconocido por el CES, estudiar 100% online a tu ritmo y aprender herramientas de Inteligencia Artificial práctica.
2. Lenguaje Persuasivo y Dinámico: Usa un tono cálido, enérgico, cercano, profesional y vendedor. Usa emojis comerciales estratégicos (🚀, 🎓, 💻, 📈, 💼, ⚡, ✨).
3. Estructura de Respuesta Vendedora:
   - Valida el interés del usuario con entusiasmo.
   - Presenta la propuesta de valor con viñetas claras y negritas.
   - Maneja cualquier duda u objeción (tiempo, costos, experiencia previa).
   - Termina SIEMPRE con una pregunta de cierre comercial (ej: "¿Te gustaría que evaluemos tu perfil para homologación?", "¿Deseas iniciar tu inscripción o prefieres que un asesor te contacte por WhatsApp para ver planes de pago?").
4. Si preguntan por precios o matrícula: Resalta el gran valor del título oficial y las facilidades de pago flexibles, e invítalo a dejar sus datos o contactar al equipo comercial de ISTCGE.

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
                full_prompt = f"{system_instruction}\n\n[CONSULTA DEL CLIENTE/POSTULANTE]:\n{prompt_text}"
                response = model_alt.generate_content(full_prompt)
                if response and response.text:
                    return response.text
            except Exception as ex:
                last_error = ex
                continue

    return f"Disculpa, ocurrió un inconveniente con el servicio de IA: {str(last_error)}"

# --- DISEÑO VISUAL COMERCIAL ISTCGE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 0%, #0d223f 0%, #050a14 100%) !important;
        font-family: 'Inter', sans-serif !important;
        color: #F8FAFC !important;
    }

    /* Ocultar elementos de Streamlit */
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Header Comercial CGE */
    .cge-header-card {
        background: linear-gradient(135deg, rgba(0, 44, 90, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(0, 156, 222, 0.35);
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }

    .cge-title-box h1 {
        color: #FFFFFF !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }

    .cge-title-box p {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        margin: 3px 0 0 0 !important;
    }

    .cge-badge-gold {
        background: linear-gradient(135deg, #FDC901, #D97706);
        color: #000000 !important;
        font-weight: 800;
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
        padding: 5px 12px;
        border-radius: 30px;
        font-size: 0.75rem;
        font-weight: 700;
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

    /* Barra Comercial de Beneficios */
    .cge-highlights-container {
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
        flex-wrap: wrap;
    }

    .cge-highlight-chip {
        background: rgba(0, 44, 90, 0.45);
        border: 1px solid rgba(0, 156, 222, 0.25);
        color: #E2E8F0 !important;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* Burbujas de Chat */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }

    /* Input */
    .stChatInputContainer {
        background-color: #0b1320 !important;
        border: 1px solid rgba(0, 156, 222, 0.4) !important;
        border-radius: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER COMERCIAL ISTCGE ---
st.markdown("""
<div class="cge-header-card">
    <div class="cge-title-box">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 2px;">
            <h1>💼 NIA • Asesora Comercial ISTCGE</h1>
            <span class="cge-badge-gold">Títulos Oficiales CES</span>
        </div>
        <p>Impulsa tu carrera con Titulación Oficial de Tercer Nivel 100% Online • Ecosistema ASCEND</p>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
        <span class="cge-badge-status">
            <span class="status-dot"></span>
            Asesora de Admisiones Activa
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- DESTACADOS COMERCIALES ---
st.markdown("""
<div class="cge-highlights-container">
    <div class="cge-highlight-chip">💻 Tec. en Desarrollo de Software</div>
    <div class="cge-highlight-chip">📈 Tec. en Ventas Digitales</div>
    <div class="cge-highlight-chip">⚡ Homologación de Experiencia Laboral</div>
    <div class="cge-highlight-chip">🧭 Test Vocacional Gratuito</div>
    <div class="cge-highlight-chip">🎓 100% Online y Flexible</div>
</div>
""", unsafe_allow_html=True)

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! 👋 Te saluda **NIA**, asesora comercial de admisiones del **Instituto Superior Tecnológico CGE (ISTCGE)**.\n\n¿Estás listo para dar el siguiente gran salto en tu carrera profesional? Te ayudo a elegir la mejor opción para ti:\n\n* 💻 **Tecnología Superior en Desarrollo de Software** *(Alta demanda y excelentes ingresos)*\n* 📈 **Tecnología Superior en Ventas Digitales** *(Domina el marketing, e-commerce y cierre de ventas)*\n* ⚡ **Homologación de Experiencia Laboral** *(¡Convalida lo que ya sabes y titúlate en tiempo récord!)*\n* 🧭 **Test Vocacional Gratuito** *(Descubre tu carrera ideal en 3 minutos)*\n\n¿Cuál de estas opciones te gustaría conocer a detalle para iniciar tu postulación?"
        }
    ]

# Renderizar mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Capturar mensaje del usuario
if prompt := st.chat_input("Escribe tu consulta sobre carreras, costos, homologación o matrícula..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if es_saludo_generico(prompt):
            reply = "¡Hola! Qué gusto saludarte. 🚀 En **ISTCGE** te ayudamos a obtener tu **Título Oficial de Tercer Nivel Tecnológico 100% en línea** con el respaldo del CES.\n\nTenemos convocatorias abiertas para:\n1. 💻 **Tecnología Superior en Desarrollo de Software**\n2. 📈 **Tecnología Superior en Ventas Digitales**\n3. ⚡ **Validación y Homologación de Experiencia Laboral** *(titulación acelerada)*\n\n¿En cuál de ellas te gustaría conocer los beneficios, plan de estudios o facilidades de pago?"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            with st.spinner("NIA está preparando tu asesoría comercial personalizada..."):
                response_text = get_gemini_response(prompt, st.session_state.messages)
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
