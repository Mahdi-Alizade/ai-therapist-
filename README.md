# MindWell AI - Cognitive Reflective Assistant

A resilient, production-ready AI cognitive companion and therapy simulator built with **FastAPI**, **Google GenAI**, and **Async SQLite**. The system implements structured Cognitive Behavioral Therapy (CBT) thought reframing, emotional distress estimation, real-time streaming, and session persistence.

---

## Architecture Overview

```text
       [ Web Client / HTML5 Single-Page App ]
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
  [ Chat Stream ]  [ Worksheets ]  [ Analytics ]
        │                │                │
        └────────────────┼────────────────┘
                         ▼
             [ FastAPI Routing Layer ]
                         │
     ┌───────────────────┼───────────────────┐
     ▼                   ▼                   ▼
[ AIService ]    [ SentimentEngine ]   [ aiosqlite Storage ]
(Google GenAI)   (Stress Analytics)   (chat_sessions, records)
Core Capabilities
Multi-Persona Behavioral Modes:

CBT Specialist (cbt): Employs Socratic questioning, identifying cognitive distortions and automatic negative thoughts.

Stoic Philosopher (stoic): Guides users through the Dichotomy of Control and rational perspective shifts.

Rubber Duck Debugger (rubber_duck): Tailored for developers tackling cognitive exhaustion, imposter syndrome, and mental blockers.

CBT Thought Record Worksheets:

Interactive 4-step modal tracking: Situation, Automatic Thought, Distortion Category (e.g., Catastrophizing, All-or-Nothing), and Balanced Reframe.

Persistent storage in SQLite with instant retrieval across sessions.

Emotional Analytics & Somatic Grounding:

Real-time client-side HTML5 canvas tracking emotional valence and stress percentages.

Embedded 4x4 Box Breathing visualizer for physiological vagus nerve regulation.

Multi-Format Session Export:

Plain text formatted session records (/api/session/{id}/export).

Clean, structured Markdown exports (/api/session/{id}/export/markdown) containing formatted tables of CBT worksheets and dialogue logs.

Operational Health & Retention:

Deep database connectivity probe integrated into /health.

Automated retention cleanup policy (cleanup_expired_sessions) to prune historical data.

Installation & Local Development
1. Virtual Environment Setup
PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
2. Environment Configuration
Create a .env file in the project root:

Code snippet
AI_API_KEY="your_actual_gemini_api_key_here"
AI_MODEL_NAME="gemini-2.5-flash"
3. Run Automated Tests
PowerShell
pytest -v
4. Start the Application
PowerShell
uvicorn app.main:app --reload --port 8000
Open http://localhost:8000 in your browser.

Containerized Deployment (Docker)
Multi-Stage Docker Build
Run the production container using the non-root runtime image:

PowerShell
docker compose up -d --build
Check running container health status:

PowerShell
docker ps --filter "name=mindwell_therapist_service"
Disclaimer
MindWell AI is an automated reflective cognitive tool, not a clinical healthcare service. In crisis situations, users should contact certified crisis helplines.