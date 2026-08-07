from pydantic import BaseModel, Field
from typing import List

class ImageMetadata(BaseModel):
    subject: str = Field(description="Primary subject, e.g., red fox, wolf")
    category: str = Field(description="Broad category, e.g., animal, nature")
    attributes: List[str] = Field(description="Key attributes, e.g., orange fur, forest")
    caption: str = Field(description="Detailed image description")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")