import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.services.database import init_database, save_session, save_message


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "service": "ai-therapist-api"}


@pytest.mark.asyncio
async def test_index_page_serves_html():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_get_session_history_flow():
    await init_database()
    test_session = "api_session_99"
    await save_session(test_session, "cbt")
    await save_message(test_session, "user", "Testing API history.")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/api/history/{test_session}")
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == test_session
        assert len(data["messages"]) == 1
        assert data["messages"][0]["content"] == "Testing API history."