from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse, Response
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
    message_dicts = [{"role": msg.role, "content": msg.content} for msg in payload.messages]
    persona_choice = payload.persona or "cbt"
    session_id = payload.session_id

    if session_id:
        await save_session(session_id, persona_choice)
        latest_user_text = payload.messages[-1].content
        await save_message(session_id, "user", latest_user_text)

    async def event_generator():
        collected_response = ""
        async for chunk in ai_service.stream_chat_response(message_dicts, persona=persona_choice):
            collected_response += chunk
            yield chunk

        if session_id and collected_response:
            await save_message(session_id, "model", collected_response)

    return StreamingResponse(event_generator(), media_type="text/plain")


@router.get("/history/{session_id}", response_model=SessionHistoryResponse)
async def get_chat_history_endpoint(session_id: str):
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
    analysis_result = analyze_text_sentiment(payload.text)

    return SentimentAnalysisResponse(
        stress_score=analysis_result["stress_score"],
        valence=analysis_result["valence"],
        detected_cues=analysis_result["detected_cues"],
        cognitive_rigidity=analysis_result["cognitive_rigidity"],
    )


@router.post("/cbt/records", response_model=ThoughtRecordItem)
async def create_thought_record_endpoint(payload: CreateThoughtRecordRequest):
    record_id = await save_thought_record(
        session_id=payload.session_id,
        situation=payload.situation,
        automatic_thought=payload.automatic_thought,
        distortion=payload.distortion,
        rational_reframe=payload.rational_reframe,
    )

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


@router.get("/session/{session_id}/export", response_class=PlainTextResponse)
async def export_session_summary_endpoint(session_id: str):
    messages = await load_session_messages(session_id)
    thought_records = await load_thought_records(session_id)

    lines = []
    lines.append("==================================================")
    lines.append("MindWell AI - Structured Reflection Session Report")
    lines.append(f"Session ID: {session_id}")
    lines.append("==================================================")
    lines.append("")
    lines.append("--- [ 1. CBT Thought Records & Cognitive Reframes ] ---")
    if not thought_records:
        lines.append("No structured worksheets recorded during this session.")
    else:
        for idx, rec in enumerate(thought_records, 1):
            lines.append(f"Worksheet #{idx}:")
            lines.append(f"  Triggering Situation: {rec['situation']}")
            lines.append(f"  Automatic Thought:    {rec['automatic_thought']}")
            lines.append(f"  Distortion Category:  {rec['distortion']}")
            lines.append(f"  Balanced Reframe:     {rec['rational_reframe']}")
            lines.append(f"  Timestamp:            {rec['created_at']}")
            lines.append("")

    lines.append("--- [ 2. Conversational Dialogue Log ] ---")
    if not messages:
        lines.append("No conversation messages logged in this session.")
    else:
        for msg in messages:
            speaker_label = "USER" if msg["role"] == "user" else "ASSISTANT"
            lines.append(f"[{speaker_label}]: {msg['content']}")
            lines.append("")

    lines.append("==================================================")
    lines.append("Notice: MindWell is an automated cognitive aid, not medical advice.")
    lines.append("==================================================")

    report_content = "\n".join(lines)
    return PlainTextResponse(
        content=report_content,
        headers={"Content-Disposition": f'attachment; filename="mindwell_session_{session_id}.txt"'}
    )


@router.get("/session/{session_id}/export/markdown", response_class=Response)
async def export_session_markdown_endpoint(session_id: str):
    messages = await load_session_messages(session_id)
    thought_records = await load_thought_records(session_id)

    md_lines = []
    md_lines.append(f"# MindWell AI - Session Report: `{session_id}`")
    md_lines.append("")
    md_lines.append("> **Disclaimer**: MindWell AI is a reflective companion and not a licensed clinical service.")
    md_lines.append("")
    md_lines.append("## 1. CBT Thought Reflection Worksheets")
    md_lines.append("")

    if not thought_records:
        md_lines.append("*No thought worksheets recorded for this session.*")
        md_lines.append("")
    else:
        md_lines.append("| # | Triggering Situation | Automatic Thought | Distortion | Rational Reframe |")
        md_lines.append("|---|----------------------|-------------------|------------|------------------|")
        for idx, item in enumerate(thought_records, 1):
            sit = item["situation"].replace("|", "/")
            at = item["automatic_thought"].replace("|", "/")
            dist = item["distortion"].replace("|", "/")
            ref = item["rational_reframe"].replace("|", "/")
            md_lines.append(f"| {idx} | {sit} | {at} | **{dist}** | {ref} |")
        md_lines.append("")

    md_lines.append("## 2. Conversational Dialogue History")
    md_lines.append("")

    if not messages:
        md_lines.append("*No messages recorded.*")
        md_lines.append("")
    else:
        for m in messages:
            role_title = "**User**" if m["role"] == "user" else "**MindWell Companion**"
            md_lines.append(f"### {role_title}")
            md_lines.append(f"{m['content']}")
            md_lines.append("")

    md_content = "\n".join(md_lines)
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="mindwell_session_{session_id}.md"'}
    )