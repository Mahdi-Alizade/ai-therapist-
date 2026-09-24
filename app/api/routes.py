from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.api.schemas import ChatRequest
from app.services.ai_service import AIService

router = APIRouter(prefix="/api", tags=["Chat"])
ai_service = AIService()


@router.post("/chat/stream")
async def chat_stream_endpoint(payload: ChatRequest):
    """
    Accepts conversation history and persona choice, streaming generated response chunks.
    """
    message_dicts = [{"role": msg.role, "content": msg.content} for msg in payload.messages]
    persona_choice = payload.persona or "cbt"

    async def event_generator():
        async for chunk in ai_service.stream_chat_response(message_dicts, persona=persona_choice):
            yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")