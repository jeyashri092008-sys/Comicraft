import re
import os

def clean_json_markdown(raw_text: str) -> str:
    text = raw_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def sanitize_filename(prompt: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9_-]', '_', prompt[:25]).strip('_')
    return f"{cleaned or 'panel'}_{abs(hash(prompt)) % 100000}.png"

def ensure_directories(*paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)
