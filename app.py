import streamlit as st
import os
import requests
import json
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
- Significado de NIA: Navega (ayuda a encontrar información), Impulsa (orienta el siguiente paso) y Asciende (acompaña a construir posibilidades).
- Sitio Web Oficial: https://web.istcge.edu.ec/
- Títulos: Títulos Oficiales de Tercer Nivel Tecnológico avalados por el Consejo de Educación Superior (CES) del Ecuador (registrados en SENESCYT).
- Modalidad: 100% en línea (virtual, asincrónica y flexible, compatible con trabajo y responsabilidades familiares).
- Slogan y Filosofía: «No solo estudies una carrera. Construye tu siguiente nivel».
- Metodología en 5 Fases: 1. Aprende -> 2. Aplica -> 3. Potencia (con IA) -> 4. Conecta (mentorías) -> 5. Asciende.

2. OFERTA DE CARRERAS OFICIALES:
A) TECNOLOGÍA SUPERIOR EN DESARROLLO DE SOFTWARE:
- Título Oficial: Tecnólogo/a Superior en Desarrollo de Software (Tercer Nivel).
- Lema: «Convierte problemas reales en soluciones digitales».
- Competencias: Programación desde cero, desarrollo web y móvil, bases de datos e Inteligencia Artificial aplicada con proyectos reales.
- Dirigido a: Bachilleres, programadores empíricos, autodidactas y técnicos que buscan título oficial y mejores ingresos.

B) TECNOLOGÍA SUPERIOR EN VENTAS DIGITALES:
- Título Oficial: Tecnólogo/a Superior en Ventas Digitales (Tercer Nivel).
- Lema: «Convierte ideas, productos y oportunidades en resultados».
- Competencias: Estrategias omnicanal, embudos de venta (funnels), marketing digital, e-commerce y CRM para disparar ventas.
- Dirigido a: Emprendedores, vendedores tradicionales, bachilleres y colaboradores comerciales.

3. RUTAS DE INGRESO Y ADMISIÓN:
- «Empieza Desde Cero»: Formación práctica desde las bases con acompañamiento continuo e IA.
- «Homologación y Validación de Experiencia Laboral»: ¡No empieces de cero! Si tienes materias aprobadas o años de experiencia en el área, convalidamos tus conocimientos para titularte en menor tiempo.
- «ISTCGE para Empresas»: Formación corporativa y convalidación para equipos de trabajo.

4. TEST VOCACIONAL ASCEND (GRATUITO Y ORIENTATIVO):
- Cuestionario de 3 minutos para explorar intereses y perfil afín: Conector Comercial (Ventas), Constructor Digital (Software), Híbrido o Explorador.
- Alcance: Es una herramienta orientativa, NO es un diagnóstico psicológico clínico ni decide por el estudiante.

5. CANALES OFICIALES DE DERIVACIÓN COMERCIAL (WHATSAPP):
- Número de WhatsApp Oficial: 099 911 5216
- Enlace directo a WhatsApp: https://wa.me/593999115216
- Cuándo derivar obligatoriamente: Consultas sobre costos vigentes, cuotas, descuentos, becas, fechas de inicio, requisitos de inscripción y prediagnóstico de asignaturas a homologar.
"""

SYSTEM_INSTRUCTION = f"""
Eres NIA, la guía virtual y asesora comercial de ISTCGE ASCEND. Tu nombre representa tres acciones: Navega, Impulsa y Asciende.
Sitio web oficial: https://web.istcge.edu.ec/

REGLAS OBLIGATORIAS DE PERSONALIDAD Y FORMATO (DOCUMENTO DE ENTRENAMIENTO OFICIAL):
1. Tono y Voz: Español claro, natural y ecuatoriano neutral. Trata siempre al usuario de "tú". Habla con calidez, entusiasmo, profesionalismo y enfoque comercial consultivo.
2. CONTINUIDAD CONVERSACIONAL (¡MUY IMPORTANTE!):
   - NUNCA vuelvas a saludar (ej: "¡Hola! Soy NIA...") si ya estás conversando con el usuario o si el usuario responde a una pregunta previa como "sí", "claro", "por favor", "cuéntame más".
   - Continúa de forma fluida la conversación respondiendo directamente a la pregunta anterior que le formulaste.
3. Regla de Emojis: Incluye EXACTAMENTE 2 a 3 emojis pertinentes por mensaje (por ejemplo: 👋, 💻, 📈, 🚀, 💬, 📲). No sobrecargues ni uses emojis decorativos excesivos.
4. Brevedad y Concisión: Responde primero lo esencial en 35 a 75 palabras aproximadamente. Una idea principal por párrafo.
5. Regla de Derivación Comercial a WhatsApp: Cuando el usuario consulte por costos vigentes, cuotas, facilidades de pago, becas, fechas de inicio, requisitos de inscripción o evaluación de homologación de materias, da una respuesta breve y DERIVA OBLIGATORIAMENTE al número oficial de WhatsApp 099 911 5216 o al enlace https://wa.me/593999115216.
6. Transparencia y Honestidad: No prometas un número exacto de materias homologadas antes del prediagnóstico oficial, ni prometas admisión o empleo garantizado. El test vocacional es strictly orientativo.
7. Cierre: Concluye siempre con una sola pregunta breve o paso de continuidad.

INFORMACIÓN INSTITUCIONAL Y COMERCIAL OFICIAL:
{KNOWLEDGE_CONTEXT}
"""

SALUDOS_GENERICOS = ["hola", "buenos dias", "buenas tardes", "buenas noches", "saludos", "hola!", "holaa", "buenas", "que tal", "hola nia"]

def es_saludo_inicial_unico(text, history):
    if len(history) > 2:
        return False
    clean = text.lower().strip().replace(".", "").replace("!", "").replace("¿", "").replace("?", "")
    return clean in SALUDOS_GENERICOS

# --- OBTENCIÓN DE CLAVES API ---
def get_api_credentials():
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key and "OPENROUTER_API_KEY" in st.secrets:
        openrouter_key = st.secrets["OPENROUTER_API_KEY"]

    if openrouter_key:
        return "openrouter", openrouter_key

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key and "GEMINI_API_KEY" in st.secrets:
        gemini_key = st.secrets["GEMINI_API_KEY"]

    if gemini_key:
        return "gemini", gemini_key

    return None, None

# --- GENERADOR OPENROUTER SSE EN TIEMPO REAL CON MODELOS LIGEROS INSTANTÁNEOS (< 1 SEGUNDO) ---
def stream_openrouter_response(history_messages, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://web.istcge.edu.ec",
        "X-Title": "NIA ISTCGE Chatbot"
    }

    # Historial completo de conversación
    messages_payload = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for msg in history_messages:
        role = "assistant" if msg["role"] == "assistant" else "user"
        messages_payload.append({"role": role, "content": msg["content"]})

    # MODELOS ULTRA-LIGEROS DE RESPUESTA INSTANTÁNEA (< 0.8s) - EXCLUIMOS MODELOS RAZONADORES LENTOS (R1)
    candidate_models = [
        "google/gemma-2-9b-it:free",
        "meta-llama/llama-3.1-8b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "qwen/qwen-2.5-7b-instruct:free",
        "openrouter/auto",
        "meta-llama/llama-3.3-70b-instruct:free"
    ]

    last_error = ""
    for model_name in candidate_models:
        payload = {
            "model": model_name,
            "messages": messages_payload,
            "temperature": 0.7,
            "max_tokens": 500,
            "stream": True
        }

        try:
            r = requests.post(url, headers=headers, json=payload, stream=True, timeout=(3, 20))
            if r.status_code == 200:
                has_yielded = False
                for line in r.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8")
                        if decoded_line.startswith("data: "):
                            json_str = decoded_line[6:].strip()
                            if json_str == "[DONE]":
                                break
                            try:
                                data = json.loads(json_str)
                                content = data["choices"][0]["delta"].get("content", "")
                                if content:
                                    has_yielded = True
                                    yield content
                            except (KeyError, IndexError, json.JSONDecodeError):
                                continue
                if has_yielded:
                    return
            else:
                last_error = f"HTTP {r.status_code}"
                continue
        except Exception as e:
            last_error = str(e)
            continue

    yield f"Disculpa, ocurrió un inconveniente momentáneo al conectar con el servidor: {last_error}"

# --- GENERADOR FALLBACK DIRECTO DE GEMINI ---
def stream_gemini_response(history_messages, api_key):
    candidate_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-latest"]
    
    contents_payload = []
    contents_payload.append({"role": "user", "parts": [{"text": f"INSTRUCCIÓN DEL SISTEMA:\n{SYSTEM_INSTRUCTION}"}]})
    contents_payload.append({"role": "model", "parts": [{"text": "Entendido. Asumiré la personalidad de NIA con memoria completa del historial de conversación."}]})

    for msg in history_messages:
        role = "model" if msg["role"] == "assistant" else "user"
        contents_payload.append({"role": role, "parts": [{"text": msg["content"]}]})

    payload = {
        "contents": contents_payload,
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 600}
    }
    headers = {"Content-Type": "application/json"}

    for model_name in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:streamGenerateContent?key={api_key}&alt=sse"
        try:
            r = requests.post(url, headers=headers, json=payload, stream=True, timeout=(3, 20))
            if r.status_code == 200:
                has_yielded = False
                for line in r.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith("data: "):
                            json_str = decoded_line[6:].strip()
                            try:
                                data = json.loads(json_str)
                                text_chunk = data["candidates"][0]["content"]["parts"][0]["text"]
                                if text_chunk:
                                    has_yielded = True
                                    yield text_chunk
                            except (KeyError, IndexError, json.JSONDecodeError):
                                continue
                if has_yielded:
                    return
        except Exception:
            continue

    yield "Disculpa, nuestros servidores de IA están procesando una alta carga. Por favor reintenta en un instante."

# --- FUNCIÓN UNIFICADA DE RESPUESTA ---
def generate_ai_response(history_messages):
    provider, key = get_api_credentials()
    if not provider:
        yield "⚠️ Por favor configura tu clave 'OPENROUTER_API_KEY' o 'GEMINI_API_KEY' en los Secrets de Streamlit."
        return

    if provider == "openrouter":
        yield from stream_openrouter_response(history_messages, key)
    else:
        yield from stream_gemini_response(history_messages, key)

# --- ESTILOS VISUALES: GAMA OFICIAL SITIO ISTCGE ASCEND ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --cge-bg-dark: #050A18;
        --cge-card-bg: #0B142B;
        --cge-cyan: #00D2FF;
        --cge-blue: #0072FF;
        --cge-gold: #FDC901;
        --cge-text-light: #F8FAFC;
        --cge-text-muted: #94A3B8;
        --cge-border: rgba(0, 210, 255, 0.28);
    }

    /* Fondo principal Deep Space */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0d1b3e 0%, #050a18 100%) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--cge-text-light) !important;
    }

    /* Ocultar barra superior y footer de Streamlit */
    header { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Ocultar avatares e iconos */
    [data-testid="stChatMessageAvatarCustom"],
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"],
    div[data-testid="stChatMessage"] > div:first-child:not([data-testid="stChatMessageContent"]) {
        display: none !important;
    }

    /* Encabezado oficial ISTCGE ASCEND */
    .ascend-header-card {
        max-width: 680px;
        margin: 0 auto 14px auto;
        padding: 16px 22px;
        background: rgba(11, 20, 43, 0.9);
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

    /* Burbujas de Mensajes */
    .stChatMessage {
        max-width: 680px !important;
        margin: 0 auto 10px auto !important;
        background: rgba(11, 20, 43, 0.9) !important;
        border: 1px solid rgba(0, 210, 255, 0.22) !important;
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

    /* Spinner de Carga */
    .stSpinner > div {
        border-top-color: #00D2FF !important;
    }
    div[data-testid="stSpinner"] {
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    /* Botones de Preguntas Frecuentes estilo ASCEND */
    div[data-testid="column"] {
        padding: 0 4px !important;
    }

    .stButton button {
        background: rgba(11, 20, 43, 0.8) !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(0, 210, 255, 0.35) !important;
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
        background: linear-gradient(135deg, rgba(0, 114, 255, 0.4), rgba(0, 210, 255, 0.25)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3) !important;
    }

    /* Eliminación de franjas e input integrado */
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottomBlockContainer"] > div,
    .stChatFloatingInputContainer,
    .stBottom {
        background: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }

    .stChatInputContainer,
    div[data-testid="stChatInput"],
    .stChatInput {
        max-width: 680px !important;
        margin: 0 auto !important;
        background: transparent !important;
    }

    div[data-testid="stChatInput"] {
        background-color: #0B142B !important;
        border: 1.5px solid #00D2FF !important;
        border-radius: 16px !important;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.5), 0 0 15px rgba(0, 210, 255, 0.25) !important;
        overflow: hidden !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #00D2FF !important;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.5), 0 0 25px rgba(0, 210, 255, 0.5) !important;
    }

    /* Texto blanco nítido al escribir */
    .stChatInputContainer textarea,
    div[data-testid="stChatInput"] textarea,
    .stChatInput textarea,
    textarea[data-testid="stChatInputTextArea"],
    textarea.st-bk {
        background-color: #0B142B !important;
        color: #FFFFFF !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        caret-color: #00D2FF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        opacity: 1 !important;
    }

    .stChatInputContainer textarea::placeholder,
    div[data-testid="stChatInput"] textarea::placeholder,
    textarea[data-testid="stChatInputTextArea"]::placeholder {
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
        font-weight: 400 !important;
    }

    div[data-testid="stChatInput"] button {
        color: #00D2FF !important;
        background: transparent !important;
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

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! 👋 Soy **NIA**, tu guía virtual de **ISTCGE ASCEND**.\n\nPuedo ayudarte a conocer nuestras **carreras oficiales de tercer nivel 100% en línea** (Desarrollo de Software y Ventas Digitales), explorar tu ruta de homologación de experiencia laboral o realizar el Test Vocacional. 🧭\n\n¿Qué te gustaría descubrir hoy? ✨"
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
        if es_saludo_inicial_unico(active_prompt, st.session_state.messages):
            reply = "¡Hola! Qué gusto saludarte. 👋 En **ISTCGE ASCEND** contamos con convocatorias abiertas para nuestras carreras oficiales de tercer nivel 100% en línea:\n\n1. 💻 **Tecnología Superior en Desarrollo de Software**\n2. 📈 **Tecnología Superior en Ventas Digitales**\n3. ⚡ **Homologación y Validación de Experiencia Laboral**\n\n¿De cuál de ellas deseas conocer los detalles o comunicarte con un asesor por WhatsApp? 📲"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            with st.spinner("NIA está consultando la información oficial de ISTCGE..."):
                full_response = st.write_stream(generate_ai_response(st.session_state.messages))
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    st.rerun()
