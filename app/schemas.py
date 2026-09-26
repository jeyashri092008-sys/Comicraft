from pydantic import BaseModel, Field
from typing import List, Optional

class PromptRequest(BaseModel):
    prompt: str = Field(..., description="Main storyline idea")
    character_name: str = Field(..., description="Protagonist name")
    setting: str = Field(..., description="Location or world setting")
    tone: str = Field(..., description="Story narrative tone")
    style: str = Field(..., description="Visual aesthetic/art style")

class PanelSchema(BaseModel):
    panel: int
    title: str
    scene_description: str
    image_prompt: str
    image_path: Optional[str] = None
    text: Optional[str] = None

class ComicResponse(BaseModel):
    status: str
    layout: List[PanelSchema]
    pdf_path: str
