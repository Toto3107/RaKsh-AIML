from pydantic import BaseModel, Field
from typing import List, Optional

class EnvironmentalEntry(BaseModel):
    parameter: str = Field(description="The name of the variable, e.g., Groundwater Level, PH, Nitrate")
    value: float = Field(description="The numeric value found in the text")
    unit: str = Field(description="The unit of measurement (e.g., mg/L, meters, index)")
    location: str = Field(description="The specific city, region, or station name")
    timestamp: str = Field(description="The date or year the data refers to (ISO format preferred)")

class VerifiedDataset(BaseModel):
    is_relevant: bool
    confidence_score: float
    extracted_data: List[EnvironmentalEntry] # This allows multiple readings from one page