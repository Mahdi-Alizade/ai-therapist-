from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.api.schemas import (
    ChatRequest,
    SessionHistoryResponse,
    ChatMessage,
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
    CreateThoughtRecordRequest,
    ThoughtRecordItem,
    ThoughtRecordListResponse,
)
from app.services.ai_service import AIService
from app.services.database import (
    save_session,
    save_message,
    load_session_messages,
    save_thought_record,
    load_thought_records,
)
from app.services.sentiment import analyze_text_sentiment

router = APIRouter(prefix="/api", tags=["Chat & CBT"])
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
        cognitive_rigidity=analysis_result["cognitive_rigidity"],
    )


@router.post("/cbt/records", response_model=ThoughtRecordItem)
async def create_thought_record_endpoint(payload: CreateThoughtRecordRequest):
    """
    Persists a structured CBT thought record (situation, automatic thought, distortion, reframe).
    """
    record_id = await save_thought_record(
        session_id=payload.session_id,
        situation=payload.situation,
        automatic_thought=payload.automatic_thought,
        distortion=payload.distortion,
        rational_reframe=payload.rational_reframe,
    )

    # Fetch recently created records to populate response object
    records = await load_thought_records(payload.session_id)
    matched = None
    for r in records:
        if r["id"] == record_id:
            matched = r
            break

    if not matched:
        raise HTTPException(status_code=500, detail="Failed to retrieve created thought record.")

    return ThoughtRecordItem(
        id=matched["id"],
        situation=matched["situation"],
        automatic_thought=matched["automatic_thought"],
        distortion=matched["distortion"],
        rational_reframe=matched["rational_reframe"],
        created_at=matched["created_at"],
    )


@router.get("/cbt/records/{session_id}", response_model=ThoughtRecordListResponse)
async def get_thought_records_endpoint(session_id: str):
    """
    Retrieves all CBT thought reflection records associated with a session.
    """
    raw_records = await load_thought_records(session_id)
    items = [
        ThoughtRecordItem(
            id=r["id"],
            situation=r["situation"],
            automatic_thought=r["automatic_thought"],
            distortion=r["distortion"],
            rational_reframe=r["rational_reframe"],
            created_at=r["created_at"],
        )
        for r in raw_records
    ]
    return ThoughtRecordListResponse(session_id=session_id, records=items)