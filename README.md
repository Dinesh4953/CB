# 🎓 Campus Bridge — AI-Powered Learning Hub & Developer Suite

[![Django Version](https://img.shields.io/badge/Django-5.2%2B-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![Bootstrap Version](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap)](https://getbootstrap.com/)
[![Render Deploy](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render)](https://cb-keoh.onrender.com)

**Campus Bridge** is a premium, state-of-the-art AI-powered Learning Management System (LMS) and developer workbench designed to supercharge student learning, multi-language coding practice, AI tutoring, document management, and career development.

---

## 🚀 Key Modules & Features

### 1. 🏗️ AI Project Architect (Laptop Only & Standalone)
A highly advanced offline/cloud developer utility that designs and sets up complete programming applications based on plain English prompts:
* **Generative Pipeline:** Utilizes LangChain coupled with cloud Groq or local Ollama models (`gpt-oss:20b`, `llama3`, `phi3`) based on system RAM.
* **Environment Compiler:** Automatically provisions virtual environments (`venv` or `npm install`) on-the-fly.
* **VS Code Launch:** Natively triggers system commands to boot up **VS Code** (`code .`) with the generated structure immediately loaded.
* *Note: Requires native system resources (Windows / macOS / Linux) and is optimized for laptop execution.*

### 2. 🤖 AI Study & Code Tutor
Integrated interactive AI chatbot with context memory powered by LangChain:
* **PDF Document RAG:** Upload any academic syllabus or textbook PDF and chat/query directly with the document's facts.
* **Smart Web Search:** Automatically searches the live web using Tavily APIs for queries demanding latest or current 2026 data.

### 3. 💻 MultiCode Compiler
A premium in-browser compilation workbench:
* **Multi-Language Support:** Write, run, and test code instantly across Python, Java, C, C++, Node.js, and React.
* **Sandbox Execution:** Executes code safely using the high-performance Judge0 API engine.

### 4. 🛠️ PDF & Image Document Tools
A robust suite of secure, local document manipulation utilities:
* **Conversions:** Convert between Text, Word, Images, and PDFs instantly.
* **OCR Support:** Extract raw text from images using PyTesseract processing.
* **PDF Utilities:** Split, compress, and merge multiple documents seamlessly in memory (never saved, keeping data private).

### 5. 👤 Profile & Codeforces Tracking
* **Codeforces Analytics:** Connect your Codeforces handle to fetch profile information, rank tiers, and automatically track your solved problem list.
* **Bio Customization:** Interactive profile dashboard with editing features.

### 6. 📄 Career Builder (CV/Resume Maker)
* Input education, skills, and work history, and generate print-ready, professional resumes with modern layouts.

---

## 🛠️ Technology Stack
* **Core:** Python, Django 5.2+, SQLite3
* **Frontend:** Vanilla CSS, JavaScript (ES6+), Bootstrap 5.3 CDN, Google Fonts (Outfit & Plus Jakarta Sans)
* **AI Orchestration:** LangChain Core, LangChain Community, Tavily Web Search API, Google Generative AI
* **Compiling Engine:** RapidAPI Judge0 Sandbox
* **Document Processing:** reportlab, python-docx, pypdf, pdf2image, pytesseract

---

## ⚙️ Installation & Local Setup

### 1️⃣ Clone the Repository & Navigate
```bash
git clone https://github.com/Dinesh4953/CB.git
cd CB/campus_bridge
```

### 2️⃣ Create & Activate a Virtual Environment
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS / Linux
python -m venv env
source env/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set up Environment Keys (Optional for Search/AI)
Create a `.env` file in the same folder as `manage.py`:
```env
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly_...
```

### 5️⃣ Run Database Migrations
```bash
python manage.py migrate
```

### 6️⃣ Launch the Development Server
```bash
python manage.py runserver
```
Visit the local workspace at `http://127.0.0.1:8000/`.

---

## 🌐 Production Deployment (Render)

To deploy this project to **Render** without pushing bulky generated static asset directories to GitHub:

### 1. Build Command on Render:
```bash
pip install -r requirements_new.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### 2. Start Command on Render:
```bash
gunicorn campus_bridge.wsgi:application
```

---

## 👨‍💻 Authors & Contributors
* **Dinesh Kumar Miriyala** — AI & ML Student | Django Developer | ML Enthusiast

---

## 📸 Interactive System Interface
* **Personalized Dashboard:** Unified access cards with glowing shining hover effects.
* **Theme Switching:** Floating toggle trigger providing a light emerald-cyan theme or pure dark luxury-gold theme.
