from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.services.database import init_database, get_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and tables upon startup
    await init_database()
    yield


app = FastAPI(
    title="MindWell AI - Therapeutic Assistant",
    description="A multi-persona cognitive companion built with FastAPI and Google GenAI",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static asset directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Register API routes
app.include_router(api_router)


@app.get("/", response_class=FileResponse)
async def serve_home_interface():
    """
    Renders the single-page application interface directly.
    """
    html_path = Path("app") / "static" / "index.html"
    return FileResponse(html_path, media_type="text/html")


@app.get("/health")
async def health_check():
    """
    Performs application and deep database health verification.
    """
    database_status = "connected"
    try:
        conn = await get_connection()
        try:
            cursor = await conn.execute("SELECT 1;")
            await cursor.fetchone()
        finally:
            await conn.close()
    except Exception:
        database_status = "unavailable"

    response_payload = {
        "status": "healthy" if database_status == "connected" else "degraded",
        "service": "ai-therapist-api",
        "database": database_status,
    }

    status_code = 200 if database_status == "connected" else 503
    return JSONResponse(content=response_payload, status_code=status_code)