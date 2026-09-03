# 🎓 NIA - Asistente Virtual y Asesor Educativo ISTCGE

Chatbot inteligente desarrollado con **Python, Streamlit, LangChain y Google Gemini**, especializado en la oferta educativa, carreras de tercer nivel tecnológico, convalidación de experiencia laboral, test vocacional y admisiones del **Instituto Superior Tecnológico CGE (ISTCGE)** y su ecosistema **ASCEND**.

---

## 🛠️ Tecnologías Utilizadas
* **Backend & UI:** Python 3.11/3.12 + Streamlit
* **Orquestador RAG:** LangChain
* **LLM Engine:** Google Gemini Flash (`gemini-1.5-flash` / `gemini-2.0-flash`)
* **Vector Store:** FAISS (Facebook AI Similarity Search)
* **Despliegue:** Streamlit Community Cloud (100% Gratis - Repositorio Privado o Público)

---

## 🚀 Despliegue en Streamlit Community Cloud (Paso a Paso)

1. Entra a **[share.streamlit.io](https://share.streamlit.io/)** e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **"Create app"** o **"New app"**.
3. Selecciona tu repositorio: **`-Nia_Chatbot_Itsce`**.
4. En **Main file path**, selecciona: `app.py`.
5. En **Advanced settings ➔ Secrets**, añade tu clave de API de Gemini:
   ```toml
   GEMINI_API_KEY = "tu_api_key_de_google_ai_studio"
   ```
6. Haz clic en **Deploy**.

---

## 🌐 Cómo Embeber en tu Página Web
Una vez desplegado en Streamlit Cloud, copia este código HTML para incrustarlo en cualquier sitio web o plataforma:

```html
<iframe
    src="https://TU-APP.streamlit.app/?embed=true"
    frameborder="0"
    width="100%"
    height="680"
    style="border: 2px solid #2563eb; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);"
    allow="clipboard-read; clipboard-write">
</iframe>
```
