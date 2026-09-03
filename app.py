import streamlit as st
import os
from dotenv import load_dotenv

# Carga de variables de entorno (.env o Secrets de Streamlit Cloud)
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# --- BASE DE CONOCIMIENTO EMBEBIDA (INFORMACIÓN OFICIAL ISTCGE / ASCEND) ---
KNOWLEDGE_CONTEXT = """
1. IDENTIDAD INSTITUCIONAL Y DATOS GENERALES:
- Nombre oficial: Instituto Superior Tecnológico CGE (ISTCGE).
- Plataforma y Ecosistema Educativo: ASCEND (Sistema de Formación Superior 100% en línea CGE-Ascend).
- Nivel Académico y Titulación: Carreras con titulación oficial de Tercer Nivel Tecnológico (Tecnologías Superiores).
- Modalidad de Estudio: 100% en línea (virtual, asincrónica y flexible, compatible con trabajo, familia y emprendimiento).
- Respaldo Normativo y Legal: Procesos académicos estructurados conforme a la normativa del Consejo de Educación Superior (CES) y las regulaciones vigentes en la República del Ecuador.
- Garantías Académicas: Evaluación por profesionales académicos especializados, respaldo docente de alta calidad, confidencialidad absoluta de la documentación.
- Slogan y Filosofía: «No solo estudies una carrera. Construye tu siguiente nivel. Integramos aprendizaje práctico, inteligencia artificial, mentorías y webinars para que avances mientras trabajas, emprendes o cuidas a los tuyos».
- Promesa de Valor: «Estudiar en línea te da flexibilidad. Crecer en un ecosistema te da mucho más. No se trata solo de estudiar en línea, se trata de avanzar con propósito y apoyo real. No tienes que detener tu vida para avanzar».

2. EL ECOSISTEMA ASCEND: METODOLOGÍA Y PILARES
Metodología de Avance en 5 Fases:
- Fase 1 - APRENDE: Contenidos interactivos de alto nivel, bases conceptuales y teóricas.
- Fase 2 - APLICA: Aprendizaje práctico aplicable de inmediato. Proyectos reales y simuladores.
- Fase 3 - POTENCIA: Integración transversal de Inteligencia Artificial (IA) y herramientas digitales avanzadas.
- Fase 4 - CONECTA: Mentorías, webinars, comunidad estudiantil y acompañamiento humano continuo.
- Fase 5 - ASCIENDE: Cumplimiento de metas profesionales, inserción laboral, ascensos y escalamiento de negocios.

Los 6 Pilares de ASCEND:
1. Formación Superior: Título oficial de tercer nivel tecnológico avalado por el CES.
2. Aprendizaje Práctico: 100% práctico basado en proyectos y simuladores.
3. Emprendimiento: Metodologías y modelos para lanzar y escalar negocios propios.
4. Inteligencia Artificial Aplicada: IA transversal para potenciar asimilación y rendimiento laboral.
5. Mentorías, Webinars y Talleres: Actividades periódicas con expertos del sector productivo.
6. Comunidad y Acompañamiento: Seguimiento docente y red de apoyo constante.

3. PROGRAMAS ACADÉMICOS (CARRERAS DISPONIBLES):
A) TECNOLOGÍA SUPERIOR EN VENTAS DIGITALES:
- Título Oficial: Tecnólogo/a Superior en Ventas Digitales (Tercer Nivel Tecnológico).
- Modalidad: 100% en línea.
- Propósito: «Convierte ideas, productos y oportunidades en resultados».
- Competencias: Estrategias comerciales omnicanal, embudos de ventas (funnels), marketing digital, e-commerce y CRM.
- Dirigido a: Emprendedores, vendedores tradicionales, bachilleres y equipos comerciales.

B) TECNOLOGÍA SUPERIOR EN DESARROLLO DE SOFTWARE:
- Título Oficial: Tecnólogo/a Superior en Desarrollo de Software (Tercer Nivel Tecnológico).
- Modalidad: 100% en línea.
- Propósito: «Convierte problemas reales en soluciones digitales».
- Competencias: Programación web y móvil, diseño de arquitecturas, bases de datos y productos digitales funcionales.
- Dirigido a: Personas desde cero, programadores empíricos/autodidactas que necesitan título oficial y profesionales técnicos.

4. RUTAS DE INGRESO Y ADMISIÓN:
A) Ruta «Empieza Desde Cero»:
- Para quienes no poseen formación previa. Formación desde las bases con acompañamiento continuo e IA.
- Perfiles: Bachilleres, Emprendedores, Trabajadores que cambian de área y exploradores vocacionales.

B) Ruta «Homologación y Validación de Experiencia»:
- Premisa: «No empieces de nuevo, empieza desde lo que ya sabes. Tu experiencia no debería ser invisible».
- Homologación de Estudios Previos: Convalidación de materias cursadas en otras universidades o institutos.
- Validación de Experiencia Laboral: Reconocimiento oficial de años de trabajo, proyectos o negocios mediante evidencias y evaluación práctica para acelerar la titulación.
- 5 Pasos: 1. Conversamos -> 2. Revisamos -> 3. Evidenciamos -> 4. Evaluamos -> 5. Creces (Ruta personalizada).

C) Ruta «ISTCGE ASCEND para Empresas» (B2B Corporativo):
- Formación corporativa y convalidación para equipos de trabajo 100% online y sin interrumpir la operatividad del negocio.

5. TEST VOCACIONAL ASCEND (GRATUITO):
- Orientación para indecisos o con presión familiar.
- 4 Perfiles resultantes: Conector Comercial (Ventas), Constructor Digital (Software), Híbrido y Explorador.

6. PREGUNTAS FRECUENTES (FAQS):
- ¿Son títulos oficiales? Sí, títulos oficiales de Tercer Nivel Tecnológico reconocidos por el Consejo de Educación Superior (CES) del Ecuador.
- ¿Requiere asistir presencialmente? No, es 100% en línea, virtual y asincrónica con máxima flexibilidad.
- ¿Cómo me inscribo o pido asesoría? A través de la página web, completando el formulario de contacto o solicitando contacto por WhatsApp con un asesor educativo oficial.
"""

SALUDOS_GENERICOS = ["hola", "buenos dias", "buenas tardes", "buenas noches", "saludos", "hola!", "holaa", "buenas", "que tal", "hola nia"]

def es_saludo_generico(text):
    clean = text.lower().strip().replace(".", "").replace("!", "").replace("¿", "").replace("?", "")
    return clean in SALUDOS_GENERICOS

@st.cache_resource
def get_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        
    if not api_key:
        st.error("⚠️ Falta configurar la variable 'GEMINI_API_KEY' en los Secrets de Streamlit.")
        st.stop()

    for model_name in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-2.5-flash"]:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                temperature=0.2,
                google_api_key=api_key
            )
            return llm
        except Exception:
            continue
            
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, google_api_key=api_key)

# --- CONFIGURACIÓN DE LA PÁGINA STREAMLIT ---
st.set_page_config(
    page_title="NIA | Asistente Virtual ISTCGE",
    page_icon="🎓",
    layout="wide"
)

# Estilos CSS Personalizados Premium
st.markdown("""
    <style>
    .stApp { 
        background: radial-gradient(circle at top, #0f172a, #020617) !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stApp, .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp li {
        color: #f1f5f9 !important;
    }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25) !important;
        backdrop-filter: blur(8px);
    }
    .stChatInputContainer {
        background-color: #0b0f19 !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
    }
    .badge-online {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(56, 189, 248, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 12px; margin-bottom: 16px;">
    <div>
        <h2 style="margin: 0; font-size: 1.5rem; color: #60a5fa !important;">✨ NIA | Asistente Virtual ISTCGE</h2>
        <p style="margin: 0; font-size: 0.85rem; color: #94a3b8 !important;">Ecosistema Formativo ASCEND • Carreras 100% Online</p>
    </div>
    <span class="badge-online">ONLINE 24/7</span>
</div>
""", unsafe_allow_html=True)

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! 👋 Soy **NIA**, la asistente virtual del **Instituto Superior Tecnológico CGE (ISTCGE)** y nuestro ecosistema **ASCEND**.\n\nEstoy aquí para orientarte sobre nuestras carreras oficiales de tercer nivel (Desarrollo de Software y Ventas Digitales), convalidación de experiencia laboral, test vocacional y beneficios. ¿En qué puedo ayudarte hoy?"
        }
    ]

# Cargar LLM
llm = get_llm()

# Prompt del sistema
system_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
Eres NIA, la asistente virtual oficial del Instituto Superior Tecnológico CGE (ISTCGE) y su ecosistema educativo ASCEND.
Tu misión es guiar y asesorar a postulantes, estudiantes y empresas con amabilidad, profesionalismo, claridad y entusiasmo.

REGLAS DE CONDUCTA:
1. Responde SIEMPRE en ESPAÑOL con un tono profesional, cercano, empático y motivador.
2. Basa tus respuestas ESTRICTAMENTE en la INFORMACIÓN INSTITUCIONAL provista abajo.
3. Formatea con negritas, listas ordenadas o con viñetas para que la respuesta sea muy amigable y fácil de leer.
4. Si algo no está en el contexto, invítalo cordialmente a comunicarse con los asesores oficiales de ISTCGE por WhatsApp o el formulario web.
5. Finaliza siempre con una pregunta cordial invitando al usuario a continuar su consulta o iniciar su proceso de admisión.

INFORMACIÓN INSTITUCIONAL OFICIAL DE ISTCGE:
{context}
"""),
    ("human", "{input}")
])

# Renderizar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Capturar interacción del usuario
if prompt := st.chat_input("Escribe tu pregunta sobre carreras, convalidación o admisión..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if es_saludo_generico(prompt):
            response = "¡Hola! Qué gusto saludarte. 😊 ¿Qué información de **ISTCGE** te gustaría consultar hoy? Puedo ayudarte con carreras, convalidación de experiencia, test vocacional o el proceso de matrícula."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            with st.spinner("NIA está consultando la información institucional..."):
                try:
                    chain = system_prompt_template | llm
                    result = chain.invoke({"context": KNOWLEDGE_CONTEXT, "input": prompt})
                    response = result.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    err_msg = f"Ocurrió un inconveniente al procesar tu consulta: {str(e)}"
                    st.error(err_msg)
