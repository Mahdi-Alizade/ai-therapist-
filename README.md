# MindWell AI (CalmSphere) 🧠✨

A robust, reflective AI therapeutic assistant built with **FastAPI**, **Google GenAI SDK**, **SQLite**, and vanilla web primitives. Engineered around Cognitive Behavioral Therapy (CBT) paradigms, multi-persona perspective exploration, proactive crisis guardrails, and real-time client sentiment analytics.

---

## 🏛️ System Architecture

```text
[ Client Web UI (Vanilla JS / CSS) ]
        │ (HTTP Stream / REST)
        ▼
[ FastAPI Routing Layer (Pydantic v2 Validation) ]
   ├── POST /api/chat/stream
   ├── GET  /api/history/{session_id}
   └── POST /api/sentiment/analyze
        │
        ├─────────────────────────────┬─────────────────────────────┐
        ▼                             ▼                             ▼
[ Crisis Guardrails ]      [ Emotion & Sentiment ]       [ SQLite Async Store ]
(Multi-language Regex)     (Valence & Stress Index)      (Sessions & Chat Log)
        │
        ▼ (Grounded Prompt Injection)
[ Multi-Persona System ]
  ├── CBT Reflective Mode (Socratic Questioning & Grounding)
  ├── Stoic Philosopher Mode (Dichotomy of Control)
  └── Rubber Duck Debugger (Burnout & Thought Unpacking)
        │
        ▼
[ Google Gemini GenAI Engine (Streaming Output) ]
🚀 Key Features
Cognitive Behavioral Therapy (CBT) Foundations: Employs Socratic dialogue, automated thought unpacking, cognitive distortion identification, and emotional validation.

Multi-Persona Perspective Switching: Seamless dynamic switching between CBT, Stoic, and Rubber Duck Debugger modes with adapted conversational contexts.

Proactive Crisis Safety Guardrails: Strict multi-lingual keyword and semantic intent monitoring (English & Persian) to intercept acute distress and provide emergency helpline referrals immediately.

Real-Time Sentiment & Stress Tracking: Algorithmic evaluation of emotional valence and cognitive rigidity markers to present real-time user stress levels.

Interactive 4x4 Box Breathing Widget: Integrated visual breathing guide to support autonomic down-regulation during heightened anxiety.

Persistent SQLite Session Storage: Async database layer (aiosqlite) tracking session histories with local device continuity.

Automated CI/CD Test Pipeline: 17+ comprehensive unit and integration tests passing on Python 3.13 via GitHub Actions.

🛠️ Tech Stack
Backend: Python 3.13, FastAPI, Uvicorn, Pydantic v2

Storage: Async SQLite (aiosqlite)

AI Model: Google GenAI SDK (Gemini)

Testing: Pytest, Pytest-Asyncio, HTTPX

Frontend: Clean Vanilla HTML5, CSS3 Glassmorphism, Modern Async JavaScript

💻 Local Setup & Execution
1. Virtual Environment Setup
PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
2. Environment Configuration
Create a .env file in the project root:

Code snippet
AI_API_KEY=your_actual_google_genai_api_key_here
AI_MODEL_NAME=gemini-2.5-flash
3. Run the Development Server
PowerShell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
Web Interface: http://127.0.0.1:8000

Interactive API Swagger Docs: http://127.0.0.1:8000/docs

🧪 Automated Testing
PowerShell
pytest -v
📜 License
This project is open-source under the MIT License.