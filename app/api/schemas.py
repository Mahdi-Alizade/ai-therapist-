from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "model", "assistant"] = Field(
        ..., description="The role of the speaker, either 'user' or 'model'"
    )
    content: str = Field(..., min_length=1, max_length=5000, description="The textual message content")


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(
        ..., min_length=1, description="List of previous conversation messages including the latest prompt"
    )
    persona: Optional[Literal["cbt", "stoic", "rubber_duck"]] = Field(
        default="cbt", description="Therapist persona style: cbt, stoic, or rubber_duck"
    )
    session_id: Optional[str] = Field(
        default=None, description="Unique session identifier for database persistence"
    )


class SessionHistoryResponse(BaseModel):
    session_id: str
    messages: List[ChatMessage]


class SentimentAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Input text to evaluate emotional metrics")


class SentimentAnalysisResponse(BaseModel):
    stress_score: float = Field(..., ge=0.0, le=1.0, description="Normalized stress and overwhelm index")
    valence: Literal["positive", "distressed", "neutral"] = Field(..., description="Overall emotional direction")
    detected_cues: List[str] = Field(default_factory=list, description="Emotional or cognitive markers identified")
    cognitive_rigidity: bool = Field(..., description="Flags presence of extreme or all-or-nothing terms")