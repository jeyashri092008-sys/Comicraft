import os
import json
import re
import google.generativeai as genai
from app.config import settings
from app.utils import clean_json_markdown

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

CANDIDATE_MODELS = [
    settings.GEMINI_MODEL,
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash"
]

def try_generate_content(prompt: str) -> str:
    for model_name in CANDIDATE_MODELS:
        if not model_name:
            continue
        clean_name = model_name if model_name.startswith("models/") else f"models/{model_name}"
        try:
            m = genai.GenerativeModel(clean_name)
            response = m.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as err:
            pass
    raise RuntimeError("Gemini models unavailable.")

def extract_character_name(full_prompt: str) -> str:
    """Extracts the user-provided character name from the prompt string."""
    match = re.search(r"The main character is\s+([^.\n]+)", full_prompt, re.IGNORECASE)
    if match:
        name = match.group(1).strip()
        if name:
            return name
    return "Hero"

def generate_outline(full_prompt: str) -> list:
    char_name = extract_character_name(full_prompt)
    prompt = f"""You are a professional AI comic planner.
Generate a strictly formatted JSON array containing 5 panel descriptions for this comic idea:

{full_prompt}

Each JSON object must have:
- "panel": integer
- "title": string
- "scene_description": string (Focus on {char_name})
- "image_prompt": string (Explicitly feature {char_name})

Respond ONLY in valid JSON:
[
  {{"panel": 1, "title": "...", "scene_description": "...", "image_prompt": "..."}}
]"""
    try:
        raw_text = try_generate_content(prompt)
        cleaned = clean_json_markdown(raw_text)
        data = json.loads(cleaned)
        if isinstance(data, list) and len(data) > 0:
            return data
    except Exception as e:
        print(f"[!] Outline fallback triggered with character: {char_name}")

    # Dynamic fallback that strictly uses YOUR custom character name
    return [
        {
            "panel": 1,
            "title": "The Boundary",
            "scene_description": f"{char_name} pauses at the edge of the mystical forest, examining the path ahead.",
            "image_prompt": f"A brave fox named {char_name} standing at the forest edge, comic art style"
        },
        {
            "panel": 2,
            "title": "Into the Deep Woods",
            "scene_description": f"{char_name} steps under the massive canopy, listening to the mysterious whispers of the trees.",
            "image_prompt": f"A fox named {char_name} walking cautiously along a mossy trail in ancient woods, cinematic comic style"
        },
        {
            "panel": 3,
            "title": "Ancient Discovery",
            "scene_description": f"{char_name} discovers an overgrown stone artifact glowing softly in the twilight.",
            "image_prompt": f"A fox named {char_name} looking at a glowing magical runic stone in a forest, comic art"
        },
        {
            "panel": 4,
            "title": "The Guardian",
            "scene_description": f"A forest spirit awakens, locking eyes with {char_name} with calm curiosity.",
            "image_prompt": f"A mystical forest creature meeting a fox named {char_name}, atmospheric lighting, comic book panel"
        },
        {
            "panel": 5,
            "title": "A New Chapter",
            "scene_description": f"With purpose renewed, {char_name} dashes toward the sunrise to continue the quest.",
            "image_prompt": f"A fox named {char_name} standing on a hill looking toward sunrise, heroic comic illustration"
        }
    ]

def generate_story(outline: list) -> str:
    # Detect the character name present in the outline
    char_name = "Hero"
    for item in outline:
        desc = item.get("scene_description", "")
        words = desc.split()
        if words:
            char_name = words[0]
            break

    summaries = [
        f"{p.get('panel', i+1)}. {p.get('title', '')}: {p.get('scene_description', '')}"
        for i, p in enumerate(outline)
    ]
    formatted_summaries = "\n".join(summaries)

    prompt = f"""You are a comic book scriptwriter.
Write an engaging narration with dialogues for these 5 panels:

{formatted_summaries}

Start each section with **Panel X: Title** so it can be split easily."""
    try:
        return try_generate_content(prompt)
    except Exception as e:
        print(f"[!] Narration fallback triggered for: {char_name}")

    story_parts = []
    for item in outline:
        num = item.get("panel", 1)
        title = item.get("title", f"Panel {num}")
        desc = item.get("scene_description", "")
        story_parts.append(
            f"**Panel {num}: {title}**\n"
            f"NARRATION: {desc}\n"
            f'{char_name.upper()}: "No matter what lies ahead, I am going to see this through."'
        )
    return "\n\n".join(story_parts)