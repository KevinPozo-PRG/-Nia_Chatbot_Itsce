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

# --- BASE DE CONOCIMIENTO INSTITUCIONAL Y COMERCIAL (ISTCGE / ASCEND) ---
KNOWLEDGE_CONTEXT = """
1. IDENTIDAD INSTITUCIONAL Y PROPUESTA DE VALOR:
- Nombre oficial: Instituto Superior Tecnológico CGE (ISTCGE) - Ecosistema Formativo ASCEND.
- Sitio Web Oficial: https://web.istcge.edu.ec/
- Títulos: Títulos Oficiales de Tercer Nivel Tecnológico avalados por el Consejo de Educación Superior (CES) del Ecuador (registrados en SENESCYT).
- Modalidad: 100% en línea (virtual, asincrónica y flexible, compatible con trabajo y responsabilidades familiares).
- Slogan: «No solo estudies una carrera. Construye tu siguiente nivel».

2. OFERTA DE CARRERAS:
A) TECNOLOGÍA SUPERIOR EN DESARROLLO DE SOFTWARE:
- Título Oficial: Tecnólogo/a Superior en Desarrollo de Software (Tercer Nivel).
- Beneficios: Programación desde cero, desarrollo web, aplicaciones móviles, bases de datos e Inteligencia Artificial aplicada con proyectos reales.
- Dirigido a: Bachilleres, programadores empíricos, autodidactas y técnicos que buscan título oficial y mejores ingresos.

B) TECNOLOGÍA SUPERIOR EN VENTAS DIGITALES:
- Título Oficial: Tecnólogo/a Superior en Ventas Digitales (Tercer Nivel).
- Beneficios: Estrategias omnicanal, embudos de venta (funnels), marketing digital, e-commerce y CRM para disparar ventas.
- Dirigido a: Emprendedores, vendedores tradicionales, bachilleres y colaboradores comerciales.

3. RUTAS DE INGRESO Y ADMISIÓN:
- «Empieza Desde Cero»: Formación práctica desde las bases con acompañamiento continuo e IA.
- «Homologación y Validación de Experiencia Laboral»: ¡No empieces de cero! Si tienes materias aprobadas o años de experiencia en el área, convalidamos tus conocimientos para titularte en menor tiempo.
- «ISTCGE para Empresas»: Formación corporativa y convalidación para equipos de trabajo.

4. TEST VOCACIONAL ASCEND (GRATUITO):
- Cuestionario orientativo de 3 minutos para descubrir tu perfil afín: Conector Comercial (Ventas), Constructor Digital (Software), Híbrido o Explorador.

5. VENTAJAS Y MANEJO DE OBJECIONES:
- Flexibilidad: Plataforma disponible 24/7 para estudiar a tu propio ritmo.
- Experiencia: No se requiere experiencia previa en programación ni ventas.
- Validez oficial: Títulos oficiales de 3er nivel legalmente avalados en Ecuador.
- Asesoría: Invitar a iniciar la matrícula o solicitar contacto por WhatsApp con un asesor oficial.
"""

SALUDOS_GENERICOS = ["hola", "buenos dias", "buenas tardes", "buenas noches", "saludos", "hola!", "holaa", "buenas", "que tal", "hola nia", "info", "informacion", "precio", "costo"]

def es_saludo_generico(text):
    clean = text.lower().strip().replace(".", "").replace("!", "").replace("¿", "").replace("?", "")
    return clean in SALUDOS_GENERICOS

# --- MODELO CACHEADO PARA VELOCIDAD ULTRA-RÁPIDA (RESPUESTA EN < 0.5s) ---
@st.cache_resource
def get_cached_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]

    if not api_key:
        return None

    genai.configure(api_key=api_key)

    system_instruction = f"""
Eres NIA, la Asesora Comercial de Admisiones y Ventas del Instituto Superior Tecnológico CGE (ISTCGE) y su plataforma educativa ASCEND.
Sitio web oficial: https://web.istcge.edu.ec/

TU ROL ES 100% COMERCIAL Y DE VENTAS:
- No eres tutora ni docente académica. Eres una ejecutiva comercial de admisiones amable, enérgica, ejecutiva y enfocada en orientar, persuadir y captar estudiantes para ISTCGE.
- Tu misión es presentar las ventajas de nuestras carreras oficiales de tercer nivel 100% en línea (Desarrollo de Software y Ventas Digitales), destacar la homologación de experiencia laboral y guiar al usuario hacia la matrícula o el contacto por WhatsApp con un asesor.

PAUTAS DE RESPUESTA:
1. Responde SIEMPRE en ESPAÑOL, con tono cálido, profesional, dinámico y vendedor.
2. Usa negritas para destacar ideas principales y listas ordenadas o con viñetas para facilitar la lectura.
3. Respuestas concisas, bien estructuradas y directas al grano (máximo 2 párrafos o viñetas claras).
4. Concluye siempre con una pregunta amable de cierre comercial invitando al siguiente paso.

INFORMACIÓN INSTITUCIONAL Y COMERCIAL:
{KNOWLEDGE_CONTEXT}
"""

    for model_name in ["gemini-flash-latest", "gemini-1.5-flash-latest", "gemini-pro", "gemini-2.0-flash", "gemini-1.5-flash"]:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            # Prueba rápida de inicialización
            return model
        except Exception:
            try:
                model_alt = genai.GenerativeModel(model_name=model_name)
                return model_alt
            except Exception:
                continue

    return genai.GenerativeModel(model_name="gemini-pro")

# --- GENERADOR DE STREAMING PARA RESPUESTAS EN TIEMPO REAL ---
def stream_gemini_response(prompt_text, model):
    if model is None:
        yield "⚠️ Por favor configura tu clave 'GEMINI_API_KEY' en los Secrets de Streamlit."
        return

    try:
        response = model.generate_content(prompt_text, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Disculpa, ocurrió un inconveniente al conectar con el servidor: {str(e)}"

# --- ESTILOS VISUALES: MINIMALISTA, SIN ÍCONOS, TEXTO DE INPUT 100% VISIBLE ---
st.markdown("""
    <style>
    /* Estilos generales limpios */
    .stApp {
        background-color: #f9fafb !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
        color: #111827 !important;
    }

    /* Ocultar barra superior y pie de página de Streamlit */
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Ocultar avatares e íconos */
    [data-testid="stChatMessageAvatarCustom"],
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"],
    div[data-testid="stChatMessage"] > div:first-child:not([data-testid="stChatMessageContent"]) {
        display: none !important;
    }

    /* Encabezado Corporativo */
    .cge-card-header {
        max-width: 680px;
        margin: 0 auto 12px auto;
        padding: 14px 18px;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .cge-header-titles h1 {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #111827 !important;
        margin: 0 !important;
        line-height: 1.2;
    }

    .cge-header-titles p {
        color: rgb(107, 114, 128) !important;
        font-size: 12.5px !important;
        margin: 2px 0 0 0 !important;
    }

    .cge-badge-status {
        background-color: #ecfdf5;
        color: #059669;
        border: 1px solid #a7f3d0;
        padding: 3px 9px;
        border-radius: 20px;
        font-size: 11.5px;
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

    /* Mensajes del chat */
    .stChatMessage {
        max-width: 680px !important;
        margin: 0 auto 8px auto !important;
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }

    .stChatMessage p, .stChatMessage li, .stChatMessage span {
        color: #1f2937 !important;
        font-size: 14px !important;
        line-height: 1.55 !important;
    }

    .stChatMessage strong {
        color: #002c5a !important;
        font-weight: 600 !important;
    }

    /* Botones de preguntas frecuentes */
    div[data-testid="column"] {
        padding: 0 3px !important;
    }

    .stButton button {
        background-color: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        padding: 7px 10px !important;
        width: 100% !important;
        text-align: left !important;
        display: block !important;
    }

    .stButton button:hover {
        border-color: #002c5a !important;
        color: #002c5a !important;
        background-color: #f8fafc !important;
    }

    /* FIX CRÍTICO: TEXTO DEL INPUT 100% VISIBLE Y LEGIBLE */
    .stChatInputContainer,
    div[data-testid="stChatInput"] {
        max-width: 680px !important;
        margin: 0 auto !important;
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }

    .stChatInputContainer textarea,
    div[data-testid="stChatInput"] textarea,
    .stChatInput textarea {
        color: #111827 !important;
        background-color: #ffffff !important;
        font-size: 14px !important;
        caret-color: #002c5a !important;
        -webkit-text-fill-color: #111827 !important;
    }

    .stChatInputContainer textarea::placeholder,
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
        -webkit-text-fill-color: #6b7280 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO MINIMALISTA PROFESIONAL ---
st.markdown("""
<div class="cge-card-header">
    <div class="cge-header-titles">
        <h1>NIA • Asesora Comercial ISTCGE</h1>
        <p>Instituto Superior Tecnológico CGE • Admisiones 100% Online</p>
    </div>
    <span class="cge-badge-status">
        <span class="status-dot"></span>
        En línea
    </span>
</div>
""", unsafe_allow_html=True)

# Cargar modelo en memoria (ultra-rápido)
model = get_cached_gemini_model()

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Te saluda **NIA**, asesora comercial de admisiones del **Instituto Superior Tecnológico CGE (ISTCGE)**.\n\nTe ayudo a elegir tu carrera de tercer nivel tecnológico 100% en línea:\n\n* **Tecnología Superior en Desarrollo de Software**\n* **Tecnología Superior en Ventas Digitales**\n* **Homologación y Validación de Experiencia Laboral** *(titulación acelerada)*\n* **Test Vocacional Gratuito**\n\n¿En cuál de nuestras opciones te gustaría recibir información sobre requisitos, plan de estudios o facilidades de pago?"
        }
    ]

# Renderizar mensajes
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- BOTONES DE PREGUNTAS FRECUENTES INTERACTIVAS AL INICIO ---
selected_prompt = None

if len(st.session_state.messages) <= 1:
    st.markdown("""
    <div style="max-width: 680px; margin: 4px auto 6px auto;">
        <p style="font-size: 12px; color: rgb(107, 114, 128); margin: 0 0 4px 0; font-weight: 500;">
            Consultas rápidas:
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎓 ¿Qué carreras ofrecen?", key="btn_carreras", use_container_width=True):
            selected_prompt = "¿Qué carreras oficiales de tercer nivel ofrecen en ISTCGE y cuáles son sus ventajas?"
        if st.button("⚡ ¿Cómo funciona la homologación?", key="btn_homologacion", use_container_width=True):
            selected_prompt = "¿Cómo funciona la validación de experiencia laboral y la homologación de materias para titularme más rápido?"
    with col2:
        if st.button("💻 Carrera de Desarrollo de Software", key="btn_software", use_container_width=True):
            selected_prompt = "Quiero información completa sobre la carrera de Tecnología Superior en Desarrollo de Software"
        if st.button("🧭 Test Vocacional Gratuito", key="btn_test", use_container_width=True):
            selected_prompt = "¿En qué consiste el Test Vocacional gratuito de ASCEND y cómo puedo realizarlo?"

# Capturar interacción por input o botón
user_input = st.chat_input("Escribe tu consulta sobre carreras, costos o matrícula...")
active_prompt = selected_prompt or user_input

if active_prompt:
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    with st.chat_message("assistant"):
        if es_saludo_generico(active_prompt):
            reply = "¡Hola! Qué gusto saludarte. En **ISTCGE** contamos con convocatorias abiertas para nuestras carreras oficiales de tercer nivel 100% en línea:\n\n1. **Tecnología Superior en Desarrollo de Software**\n2. **Tecnología Superior en Ventas Digitales**\n3. **Homologación y Validación de Experiencia Laboral**\n\n¿De cuál de ellas deseas conocer los detalles o facilidades de pago?"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            # Respuesta instantánea con Streaming en tiempo real
            full_response = st.write_stream(stream_gemini_response(active_prompt, model))
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    st.rerun()
