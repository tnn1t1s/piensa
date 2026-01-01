"""Choice extraction models for Asian Disease Problem responses."""

from enum import Enum
from pydantic import BaseModel, Field


class Choice(str, Enum):
    """Possible choices in the Asian Disease Problem."""
    A = "A"
    B = "B"
    UNCLEAR = "unclear"
    REFUSED = "refused"


class ChoiceExtraction(BaseModel):
    """Structured extraction of choice from model response."""

    choice: Choice = Field(
        description="The medicine/program choice extracted from the response"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in extraction (0-1)"
    )
    reasoning: str = Field(
        description="Brief explanation of how choice was determined"
    )
