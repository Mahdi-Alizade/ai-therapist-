from typing import AsyncGenerator, List, Dict
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.prompts import SYSTEM_INSTRUCTION
from app.services.safety import evaluate_crisis_risk


class AIService:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.AI_API_KEY)
        self.model_name = settings.AI_MODEL_NAME

    async def stream_chat_response(
        self,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """
        Takes conversation history, checks crisis guardrails on the latest message,
        and streams the response from the AI model.
        """
        if not messages:
            yield "No message provided."
            return

        latest_user_message = messages[-1].get("content", "")
        crisis_alert = evaluate_crisis_risk(latest_user_message)
        if crisis_alert:
            yield crisis_alert
            return

        contents = []
        for msg in messages:
            role = "user" if msg.get("role") == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg.get("content", ""))]
                )
            )

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,
            max_output_tokens=800,
        )

        try:
            response_stream = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=config,
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        except Exception as exc:
            yield f"Error generating response: {str(exc)}"