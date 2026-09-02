from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.api.schemas import ChatRequest
from app.services.ai_service import AIService

router = APIRouter(prefix="/api", tags=["Chat"])
ai_service = AIService()


@router.post("/chat/stream")
async def chat_stream_endpoint(payload: ChatRequest):
    """
    Accepts conversation history and streams generated response chunks in real-time.
    """
    message_dicts = [{"role": msg.role, "content": msg.content} for msg in payload.messages]

    async def event_generator():
        async for chunk in ai_service.stream_chat_response(message_dicts):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")