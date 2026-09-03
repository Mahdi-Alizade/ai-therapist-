# CalmSphere AI 🌿

An empathetic, active-listening AI conversational agent built with FastAPI and modern LLM streaming capabilities, engineered with explicit safety boundaries and automated crisis-intervention guardrails.

---

## ⚠️ Important Disclaimer

**CalmSphere is an experimental AI demonstration and NOT a licensed medical, psychological, or healthcare service.** It is strictly designed for reflective, active-listening exercises. It cannot provide clinical diagnoses, medical advice, or psychiatric treatment. If you or someone you know is in crisis, please immediately reach out to local emergency services or professional crisis support networks (such as 988 in the US/Canada, 111 in the UK, or 123 in Iran).

---

## 🏗️ Architecture & Features

- **Asynchronous Streaming Engine:** Native Server-Sent Events (SSE) integration delivering low-latency token generation to the client.
- **Safety First (Crisis Guardrails):** Real-time pattern interception that prevents unsafe prompts from hitting the model and serves emergency helpline resources immediately.
- **Clean Architecture:** Strict decoupling between System Prompts, Core Business Logic, Safety Interceptors, and API Schemas.
- **Zero Front-End Build Complexity:** Responsive, modern dark-mode interface served directly via static ASGI mounts.
- **Config Validation:** Environment-driven settings powered by Pydantic BaseSettings.

---

## 📂 Project Structure

```text
ai-therapist/
├── app/
│   ├── api/
│   │   ├── routes.py          # Chat streaming and API endpoints
│   │   └── schemas.py         # Pydantic input/output contracts
│   ├── core/
│   │   ├── config.py          # Environment settings
│   │   └── prompts.py         # System persona & reflection guardrails
│   ├── services/
│   │   ├── ai_service.py      # LLM connection & token streaming
│   │   └── safety.py          # Pattern matching & crisis evaluation
│   ├── static/
│   │   └── index.html         # Responsive web interface
│   └── main.py                # ASGI application root
├── tests/
│   ├── test_api.py            # Route verification tests
│   └── test_safety.py         # Guardrail unit tests
├── .env.example               # Config blueprint
├── .gitignore                 # Version control hygiene
├── requirements.txt           # Production & testing dependencies
└── README.md                  # Project documentation
🚀 Quick Start
1. Prerequisites
Python 3.10+

An API Key from an AI provider (e.g., Google AI Studio)

2. Setup Environment
Bash
# Clone the repository
git clone [https://github.com/your-username/ai-therapist.git](https://github.com/your-username/ai-therapist.git)
cd ai-therapist

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1    # On Windows PowerShell
# source venv/bin/activate     # On Linux/macOS
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Variables
Copy the template file to .env:

PowerShell
cp .env.example .env
Open .env and set your API key:

Code snippet
AI_API_KEY=your_actual_key_here
AI_MODEL_NAME=gemini-2.5-flash
5. Run the Server
Bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
Open your browser and navigate to http://127.0.0.1:8000.

🧪 Testing
Execute automated unit and integration tests with pytest:

PowerShell
pytest -v
📄 License
This repository is licensed under the MIT License.
