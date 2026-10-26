from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.api.schemas import (
    ChatRequest,
    SessionHistoryResponse,
    ChatMessage,
    SentimentAnalysisRequest,
    SentimentAnalysisResponse
)
from app.services.ai_service import AIService
from app.services.database import save_session, save_message, load_session_messages
from app.services.sentiment import analyze_text_sentiment

router = APIRouter(prefix="/api", tags=["Chat"])
ai_service = AIService()


@router.post("/chat/stream")
async def chat_stream_endpoint(payload: ChatRequest):
    """
    Accepts conversation history and persona choice, streaming generated response chunks.
    Persists messages to SQLite if session_id is provided.
    """
    message_dicts = [{"role": msg.role, "content": msg.content} for msg in payload.messages]
    persona_choice = payload.persona or "cbt"
    session_id = payload.session_id

    # Persist the latest user message if session tracking is active
    if session_id:
        await save_session(session_id, persona_choice)
        latest_user_text = payload.messages[-1].content
        await save_message(session_id, "user", latest_user_text)

    async def event_generator():
        collected_response = ""
        async for chunk in ai_service.stream_chat_response(message_dicts, persona=persona_choice):
            collected_response += chunk
            yield chunk

        # Persist full assistant response at the completion of stream
        if session_id and collected_response:
            await save_message(session_id, "model", collected_response)

    return StreamingResponse(event_generator(), media_type="text/plain")


@router.get("/history/{session_id}", response_model=SessionHistoryResponse)
async def get_chat_history_endpoint(session_id: str):
    """
    Retrieves stored message history for a given session.
    """
    raw_messages = await load_session_messages(session_id)
    if not raw_messages:
        return SessionHistoryResponse(session_id=session_id, messages=[])

    formatted_messages = [
        ChatMessage(role=item["role"], content=item["content"])
        for item in raw_messages
    ]
    return SessionHistoryResponse(session_id=session_id, messages=formatted_messages)


@router.post("/sentiment/analyze", response_model=SentimentAnalysisResponse)
async def analyze_sentiment_endpoint(payload: SentimentAnalysisRequest):
    """
    Analyzes emotional valence, stress index, and cognitive rigidity of the provided text.
    """
    analysis_result = analyze_text_sentiment(payload.text)
    
    return SentimentAnalysisResponse(
        stress_score=analysis_result["stress_score"],
        valence=analysis_result["valence"],
        detected_cues=analysis_result["detected_cues"],
        cognitive_rigidity=analysis_result["cognitive_rigidity"]
    )