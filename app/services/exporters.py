import os
from datetime import datetime
from fpdf import FPDF
from app.config import settings

def save_pdf(layout: list) -> str:
    os.makedirs(settings.EXPORTS_DIR, exist_ok=True)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", style="B", size=15)
        title = f"Panel {panel['panel']}: {panel.get('title', '')}"
        pdf.cell(0, 10, text=title.encode("latin-1", "replace").decode("latin-1"), new_x="LMARGIN", new_y="NEXT", align="C")

        y_image = 30
        img_height = 100
        rel_img_path = panel.get("image_path", "").lstrip("/")
        abs_img_path = os.path.join(settings.BASE_DIR, rel_img_path)

        if os.path.exists(abs_img_path):
            pdf.image(abs_img_path, x=10, y=y_image, w=pdf.epw, h=img_height)
        else:
            pdf.set_y(y_image)
            pdf.multi_cell(0, 10, f"Image not found at {abs_img_path}")

        pdf.set_y(y_image + img_height + 15)
        pdf.set_font("Helvetica", size=11)
        story_content = panel.get("text", "").encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 7, text=story_content)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    full_path = os.path.join(settings.EXPORTS_DIR, filename)
    pdf.output(full_path)
    return f"/static/exports/{filename}"
