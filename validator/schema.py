from pydantic import BaseModel, Field
from typing import List, Optional

class VerifiedData(BaseModel):
    is_valid: bool = Field(description="Is this data reliable and relevant?")
    confidence_score: float = Field(description="Score from 0.0 to 1.0")
    cleaned_text: str = Field(description="The text with ads/noise removed")
    entities: List[str] = Field(description="Key topics found (e.g., 'Groundwater', 'Punjab')")
    skeptic_notes: Optional[str] = Field(description="Any red flags found by the Skeptic")