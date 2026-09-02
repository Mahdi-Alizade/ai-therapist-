from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import router as chat_router

app = FastAPI(
    title="CalmSphere AI Assistant",
    description="An empathetic active-listening AI assistant experiment with built-in crisis guardrails.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=FileResponse)
async def serve_index():
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-therapist-api"}