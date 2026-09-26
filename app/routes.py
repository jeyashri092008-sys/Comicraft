import traceback
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.schemas import PromptRequest, ComicResponse
from app.services.gemini import generate_outline, generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

@router.get("/", response_class=HTMLResponse)
async def index_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@router.post("/generate", response_class=HTMLResponse)
async def generate_view(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...)
):
    try:
        meta_prompt = (
            f"The main character is {character_name}.\n"
            f"The setting is {setting}.\n"
            f"The tone is {tone}. The art style is {style}.\n"
            f"Story: {prompt}"
        )

        outline = generate_outline(meta_prompt)
        full_story = generate_story(outline)
        images = [generate_image(f"{p.get('image_prompt', prompt)}, {style} style") for p in outline]
        layout = build_comic_layout(images, full_story, outline)
        pdf_path = save_pdf(layout)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout,
                "pdf_path": pdf_path
            }
        )
    except Exception as e:
        traceback.print_exc()
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error_message": str(e)},
            status_code=500
        )

@router.post("/generate-comic/json", response_model=ComicResponse)
async def generate_comic_api(data: PromptRequest):
    try:
        meta_prompt = (
            f"The main character is {data.character_name}.\n"
            f"The setting is {data.setting}.\n"
            f"The tone is {data.tone}. The art style is {data.style}.\n"
            f"Story: {data.prompt}"
        )
        outline = generate_outline(meta_prompt)
        full_story = generate_story(outline)
        images = [generate_image(f"{p.get('image_prompt', data.prompt)}, {data.style} style") for p in outline]
        layout = build_comic_layout(images, full_story, outline)
        pdf_path = save_pdf(layout)

        return ComicResponse(status="success", layout=layout, pdf_path=pdf_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success_view(request: Request, pdf_path: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_path": pdf_path}
    )

@router.get("/test-image")
async def test_image_endpoint(prompt: str = "A futuristic cybernetic fox in neon forest, digital art"):
    try:
        path = generate_image(prompt)
        return {"status": "success", "image_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))