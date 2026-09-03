import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carga de variables de entorno
load_dotenv()

# --- CONFIGURACIÓN DE PÁGINA STREAMLIT ---
st.set_page_config(
    page_title="NIA | Asesora Comercial ISTCGE - ASCEND",
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
- Slogan y Filosofía: «No solo estudies una carrera. Construye tu siguiente nivel».
- Metodología en 5 Fases: 1. Aprende -> 2. Aplica -> 3. Potencia (con IA) -> 4. Conecta (mentorías) -> 5. Asciende.

2. OFERTA DE CARRERAS:
A) TECNOLOGÍA SUPERIOR EN DESARROLLO DE SOFTWARE:
- Título Oficial: Tecnólogo/a Superior en Desarrollo de Software (Tercer Nivel).
- Lema: «Convierte problemas reales en soluciones digitales».
- Beneficios: Programación desde cero, desarrollo web y móvil, bases de datos e Inteligencia Artificial aplicada con proyectos reales para armar tu portafolio.
- Dirigido a: Bachilleres, programadores empíricos, autodidactas y técnicos que buscan título oficial y mejores ingresos.

B) TECNOLOGÍA SUPERIOR EN VENTAS DIGITALES:
- Título Oficial: Tecnólogo/a Superior en Ventas Digitales (Tercer Nivel).
- Lema: «Convierte ideas, productos y oportunidades en resultados».
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

# --- MODELO CACHEADO GEMINI (OFICIAL 3.6-FLASH) ---
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

    models_to_try = [
        "models/gemini-3.6-flash",
        "gemini-3.6-flash",
        "models/gemini-2.0-flash",
        "gemini-2.0-flash",
        "models/gemini-1.5-flash",
        "gemini-1.5-flash",
        "models/gemini-pro"
    ]

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            return model
        except Exception:
            try:
                model_alt = genai.GenerativeModel(model_name=model_name)
                model_alt.generate_content("test", generation_config={"max_output_tokens": 1})
                return model_alt
            except Exception:
                continue

    return genai.GenerativeModel(model_name="models/gemini-3.6-flash")

# --- GENERADOR DE STREAMING EN TIEMPO REAL ---
def stream_gemini_response(prompt_text, model):
    if model is None:
        yield "⚠️ Por favor configura tu clave 'GEMINI_API_KEY' en los Secrets de Streamlit."
        return

    try:
        full_prompt = f"""
[CONSULTA DEL PROSPECTO]:
{prompt_text}

Recuerda responder como NIA, asesora comercial de ISTCGE, guiando al postulante con la información oficial de las carreras y orientándolo hacia la matrícula o el contacto por WhatsApp.
"""
        response = model.generate_content(full_prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Disculpa, ocurrió un inconveniente al conectar con el servidor: {str(e)}"

# --- PALETA Y ESTILOS OFICIALES DEL SITIO ISTCGE ASCEND (DEL PDF OFICIAL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Variables Oficiales ISTCGE ASCEND */
    :root {
        --cge-bg-dark: #050A18;
        --cge-card-bg: #0B142B;
        --cge-cyan: #00D2FF;
        --cge-blue: #0072FF;
        --cge-gold: #FDC901;
        --cge-text-light: #F8FAFC;
        --cge-text-muted: #94A3B8;
        --cge-border: rgba(0, 210, 255, 0.25);
    }

    /* Fondo Deep Space Navy oficial */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0d1b3e 0%, #050a18 100%) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--cge-text-light) !important;
    }

    /* Ocultar barra superior y footer */
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Ocultar avatares e iconos molestos */
    [data-testid="stChatMessageAvatarCustom"],
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"],
    div[data-testid="stChatMessage"] > div:first-child:not([data-testid="stChatMessageContent"]) {
        display: none !important;
    }

    /* Encabezado con paleta oficial ISTCGE ASCEND */
    .ascend-header-card {
        max-width: 680px;
        margin: 0 auto 14px auto;
        padding: 16px 22px;
        background: rgba(11, 20, 43, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--cge-border);
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 210, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .ascend-header-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .ascend-logo-badge {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #0072FF 0%, #00D2FF 100%);
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 14px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
        letter-spacing: 0.5px;
    }

    .ascend-titles h1 {
        font-size: 16px !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        margin: 0 !important;
        letter-spacing: -0.3px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .ascend-titles p {
        color: var(--cge-text-muted) !important;
        font-size: 12.5px !important;
        margin: 2px 0 0 0 !important;
        font-weight: 500;
    }

    .ascend-gold-pill {
        background: linear-gradient(135deg, #FDC901, #EAB308);
        color: #000000 !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 0 10px rgba(253, 201, 1, 0.3);
    }

    .ascend-status-pill {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.35);
        padding: 4px 10px;
        border-radius: 30px;
        font-size: 11.5px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    .pulse-dot {
        width: 6px;
        height: 6px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10B981;
    }

    /* Burbujas de Mensajes estilo Tarjeta Oscura Neón CGE */
    .stChatMessage {
        max-width: 680px !important;
        margin: 0 auto 10px auto !important;
        background: rgba(11, 20, 43, 0.85) !important;
        border: 1px solid rgba(0, 210, 255, 0.18) !important;
        border-radius: 16px !important;
        padding: 14px 20px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px);
    }

    .stChatMessage p, .stChatMessage li, .stChatMessage span {
        color: #F1F5F9 !important;
        font-size: 14.5px !important;
        line-height: 1.6 !important;
        font-weight: 450;
    }

    .stChatMessage strong {
        color: var(--cge-cyan) !important;
        font-weight: 700 !important;
    }

    /* Botones de Preguntas Frecuentes estilo ASCEND */
    div[data-testid="column"] {
        padding: 0 4px !important;
    }

    .stButton button {
        background: rgba(11, 20, 43, 0.75) !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
        border-radius: 12px !important;
        font-size: 12.5px !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
        width: 100% !important;
        text-align: left !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }

    .stButton button:hover {
        border-color: var(--cge-cyan) !important;
        color: #FFFFFF !important;
        background: linear-gradient(135deg, rgba(0, 114, 255, 0.4), rgba(0, 210, 255, 0.2)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.25) !important;
    }

    /* Barra de Input con Paleta Oficial e Iluminación Cyan */
    .stChatInputContainer,
    div[data-testid="stChatInput"],
    .stChatInput,
    [data-testid="stBottomBlockContainer"] {
        max-width: 680px !important;
        margin: 0 auto !important;
        background-color: transparent !important;
    }

    div[data-testid="stChatInput"] {
        background: rgba(11, 20, 43, 0.95) !important;
        border: 1.5px solid rgba(0, 210, 255, 0.4) !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 15px rgba(0, 210, 255, 0.15) !important;
        overflow: hidden !important;
        transition: all 0.2s ease;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: var(--cge-cyan) !important;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.35) !important;
    }

    /* TEXTO NÍTIDO BLANCO EN EL INPUT */
    .stChatInputContainer textarea,
    div[data-testid="stChatInput"] textarea,
    .stChatInput textarea,
    textarea[data-testid="stChatInputTextArea"],
    textarea.st-bk {
        background-color: transparent !important;
        color: #FFFFFF !important;
        font-size: 14.5px !important;
        font-weight: 500 !important;
        caret-color: var(--cge-cyan) !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
    }

    .stChatInputContainer textarea::placeholder,
    div[data-testid="stChatInput"] textarea::placeholder,
    textarea[data-testid="stChatInputTextArea"]::placeholder {
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
        font-weight: 450;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER OFICIAL ISTCGE ASCEND ---
st.markdown("""
<div class="ascend-header-card">
    <div class="ascend-header-left">
        <div class="ascend-logo-badge">CGE</div>
        <div class="ascend-titles">
            <h1>NIA • Asesora Oficial ISTCGE <span class="ascend-gold-pill">CES</span></h1>
            <p>Ecosistema Formativo ASCEND • Carreras Oficiales 100% Online</p>
        </div>
    </div>
    <span class="ascend-status-pill">
        <span class="pulse-dot"></span>
        En línea
    </span>
</div>
""", unsafe_allow_html=True)

# Cargar modelo verificado (gemini-3.6-flash)
model = get_cached_gemini_model()

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! Te saluda **NIA**, asesora comercial de admisiones del **Instituto Superior Tecnológico CGE (ISTCGE)** y nuestro ecosistema **ASCEND**.\n\n¿Listo para construir tu siguiente nivel profesional? Te ayudo a elegir tu carrera oficial de tercer nivel 100% en línea:\n\n* **Tecnología Superior en Desarrollo de Software** *(Alta demanda, bases de datos y desarrollo con IA)*\n* **Tecnología Superior en Ventas Digitales** *(Domina e-commerce, funnels y cierre omnicanal)*\n* **Homologación de Experiencia Laboral** *(¡Convalida tus conocimientos y titúlate en menor tiempo!)*\n* **Test Vocacional Gratuito** *(Descubre tu perfil afín en 3 minutos)*\n\n¿En cuál de nuestras opciones te gustaría recibir información sobre requisitos o facilidades de pago?"
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
    <div style="max-width: 680px; margin: 4px auto 8px auto;">
        <p style="font-size: 12px; color: #94A3B8; margin: 0 0 6px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
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
