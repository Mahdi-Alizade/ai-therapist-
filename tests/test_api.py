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


@pytest.mark.asyncio
async def test_sentiment_analysis_api_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"text": "I feel anxious and overwhelmed by this situation."}
        response = await client.post("/api/sentiment/analyze", json=payload)
        assert response.status_code == 200
        result = response.json()
        assert result["valence"] == "distressed"
        assert result["stress_score"] > 0.0
        assert "anxious" in result["detected_cues"] or "overwhelmed" in result["detected_cues"]


@pytest.mark.asyncio
async def test_thought_record_create_and_list_flow():
    await init_database()
    test_session_id = "sess_thought_test_101"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create record
        payload = {
            "session_id": test_session_id,
            "situation": "Presenting code review in front of senior engineers",
            "automatic_thought": "I will mess up and everyone will think I am incompetent",
            "distortion": "Catastrophizing / Fortune Telling",
            "rational_reframe": "I prepared well and questions are a normal part of collaboration, not an attack."
        }
        create_res = await client.post("/api/cbt/records", json=payload)
        assert create_res.status_code == 200
        record_data = create_res.json()
        assert record_data["id"] > 0
        assert record_data["situation"] == payload["situation"]

        # List records for session
        list_res = await client.get(f"/api/cbt/records/{test_session_id}")
        assert list_res.status_code == 200
        list_data = list_res.json()
        assert list_data["session_id"] == test_session_id
        assert len(list_data["records"]) >= 1
        assert list_data["records"][0]["distortion"] == payload["distortion"]