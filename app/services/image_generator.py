import os
import io
import time
import urllib.parse
import requests
from PIL import Image
from app.config import settings
from app.utils import sanitize_filename

def crop_watermark(image: Image.Image) -> Image.Image:
    """Trims the bottom watermark strip cleanly."""
    width, height = image.size
    # Crop out the bottom 32 pixels where the watermark renders
    cut_height = max(100, height - 32)
    return image.crop((0, 0, width, cut_height))

def generate_image_pollinations(prompt: str, full_path: str) -> bool:
    clean_prompt = prompt[:160].replace("\n", " ").strip()
    encoded = urllib.parse.quote(clean_prompt)
    
    # Passing &nologo=true &nofeed=true suppresses branding
    seed = int(time.time() * 1000) % 99999
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=384&model=turbo&nologo=true&nofeed=true&seed={seed}"

    for attempt in range(3):
        try:
            res = requests.get(url, timeout=45)
            if res.status_code == 200 and len(res.content) > 1000:
                img = Image.open(io.BytesIO(res.content))
                # Crop any remaining logo imprint cleanly off the bottom
                img_cleaned = crop_watermark(img)
                img_cleaned.save(full_path)
                print(f"[✓] Image generated and watermark removed for: {clean_prompt[:30]}...")
                return True
        except Exception as e:
            print(f"[!] Attempt {attempt + 1} retry: {e}")
            time.sleep(1)
    return False

def generate_image(prompt: str, filename: str = None) -> str:
    if not filename:
        filename = sanitize_filename(prompt)
    
    os.makedirs(settings.PANELS_DIR, exist_ok=True)
    full_path = os.path.join(settings.PANELS_DIR, filename)
    rel_path = f"/static/panels/{filename}"

    success = generate_image_pollinations(prompt, full_path)

    if not success and not os.path.exists(full_path):
        img = Image.new("RGB", (512, 352), color=(40, 50, 65))
        img.save(full_path)

    return rel_path