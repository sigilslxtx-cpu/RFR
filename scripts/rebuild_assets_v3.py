from pathlib import Path
import re
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "assets" / "examples"

IMAGE_MAP = {
    "business/08.27.26.v2_pepper_riot_downloads_before_after_final.webp": "business/08.27.26.v3_pepper_riot_downloads_before_after_final.webp",
    "business/08.27.26.v2_pepper_riot_drive_before_after_final.webp": "business/08.27.26.v3_pepper_riot_drive_before_after_final.webp",
    "business/08.27.26.v2_pepper_riot_sales_orders_receipts_before_after_final.webp": "business/08.27.26.v3_pepper_riot_sales_orders_receipts_before_after_final.webp",
    "personal/08.27.26.v2_personal_downloads_before_after_final.webp": "personal/08.27.26.v3_personal_downloads_before_after_final.webp",
    "personal/08.27.26.v2_personal_drive_before_after_final.webp": "personal/08.27.26.v3_personal_drive_before_after_final.webp",
    "personal/08.27.26.v2_personal_mixed_scanning_before_after_final.webp": "personal/08.27.26.v3_personal_mixed_scanning_before_after_final.webp",
    "chat/08.27.26.v2_RFR_Chat_Extraction_Before_After.webp": "chat/08.27.26.v3_RFR_Chat_Extraction_Before_After.webp",
    "chat/08.27.26.v2_RFR_Full_C2D_Before_After.webp": "chat/08.27.26.v3_RFR_Full_C2D_Before_After.webp",
    "general/08.27.26.v2_RFR_Digital_File_Rescue_Before_After.webp": "general/08.27.26.v3_RFR_Digital_File_Rescue_Before_After.webp",
}


def flatten_rgb(im):
    if im.mode in ("RGBA", "LA") or "transparency" in im.info:
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im.convert("RGBA"))
        return bg.convert("RGB")
    return im.convert("RGB")


def edit_image(src_rel, dst_rel):
    src = EXAMPLES / src_rel
    dst = EXAMPLES / dst_rel
    im = flatten_rgb(Image.open(src))
    draw = ImageDraw.Draw(im)

    if "Digital_File_Rescue" in src_rel:
        bg = im.getpixel((20, 20))
        # Remove promotional subtitle, footer, and handwritten slogan.
        draw.rectangle((55, 140, 880, 182), fill=bg)
        draw.rectangle((45, 602, 1100, 642), fill=bg)
        draw.rectangle((1240, 370, 1540, 465), fill=bg)
    elif "Chat_Extraction" in src_rel:
        bg = im.getpixel((20, 20))
        draw.rectangle((60, 165, 1000, 204), fill=bg)
        draw.rectangle((50, 825, 1120, 868), fill=bg)
    elif "Full_C2D" in src_rel:
        bg = im.getpixel((20, 20))
        draw.rectangle((60, 165, 1230, 204), fill=bg)
        draw.rectangle((50, 825, 1200, 868), fill=bg)
    elif "personal_mixed_scanning" in src_rel:
        bg = im.getpixel((10, 500))
        draw.rectangle((560, 480, 980, 514), fill=bg)
        draw.rectangle((375, 945, 1160, 1008), fill=bg)

    max_width = 1200
    if im.width > max_width:
        new_height = round(im.height * max_width / im.width)
        im = im.resize((max_width, new_height), Image.Resampling.LANCZOS)

    dst.parent.mkdir(parents=True, exist_ok=True)
    # Standard lossy VP8 WebP for broad mobile-browser compatibility.
    im.save(dst, "WEBP", quality=84, method=4, lossless=False)
    return dst


def pdf_path_for(image_path):
    category = image_path.parent.name
    if category == "business":
        folder = ROOT / "samples" / "pepper-riot"
    elif category == "personal":
        folder = ROOT / "samples" / "personal"
    else:
        folder = ROOT / "samples" / "general"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{image_path.stem}.pdf"


def make_pdf(image_path):
    im = Image.open(image_path).convert("RGB")
    temp_jpg = ROOT / ".rfr_pdf_temp.jpg"
    im.save(temp_jpg, "JPEG", quality=80, optimize=True, progressive=False)
    pdf_path = pdf_path_for(image_path)
    width, height = im.size
    c = canvas.Canvas(str(pdf_path), pagesize=(width * 0.5, height * 0.5), pageCompression=1)
    c.drawImage(str(temp_jpg), 0, 0, width=width * 0.5, height=height * 0.5)
    c.showPage()
    c.save()
    temp_jpg.unlink(missing_ok=True)
    return pdf_path


def rebuild_logos():
    brand = ROOT / "assets" / "brand"
    for variant in ("Horizontal_Black", "Horizontal_Color", "Horizontal_White"):
        old = brand / f"08.27.26_RFR_Logo_{variant}.svg"
        new = brand / f"08.27.26.v2_RFR_Logo_{variant}.svg"
        text = old.read_text(encoding="utf-8")
        text = re.sub(r'\n?<text x="252" y="139".*?</text>', "", text)
        text = re.sub(r'\n?<text x="252" y="164".*?</text>', "", text)
        new.write_text(text, encoding="utf-8")
        old.unlink()


def update_html():
    path = ROOT / "index.html"
    html = path.read_text(encoding="utf-8")
    html = html.replace("08.27.26_RFR_Logo_Horizontal_Color.svg", "08.27.26.v2_RFR_Logo_Horizontal_Color.svg")
    html = html.replace("08.27.26_RFR_Logo_Horizontal_White.svg", "08.27.26.v2_RFR_Logo_Horizontal_White.svg")
    html = html.replace("08.27.26.v2_pepper_riot_", "08.27.26.v3_pepper_riot_")
    html = html.replace("08.27.26.v2_personal_", "08.27.26.v3_personal_")
    html = html.replace("08.27.26.v2_RFR_Chat_Extraction_Before_After.webp", "08.27.26.v3_RFR_Chat_Extraction_Before_After.webp")
    html = html.replace("08.27.26.v2_RFR_Full_C2D_Before_After.webp", "08.27.26.v3_RFR_Full_C2D_Before_After.webp")
    html = html.replace("08.27.26.v2_RFR_Digital_File_Rescue_Before_After.webp", "08.27.26.v3_RFR_Digital_File_Rescue_Before_After.webp")
    path.write_text(html, encoding="utf-8")


def remove_old_visual_pdfs():
    for folder in (ROOT / "samples" / "general", ROOT / "samples" / "pepper-riot", ROOT / "samples" / "personal"):
        if folder.exists():
            for p in folder.glob("08.27.26.v2_*Before_After.pdf"):
                p.unlink()
            for p in folder.glob("08.27.26.v2_*before_after_final.pdf"):
                p.unlink()


if __name__ == "__main__":
    rebuilt = []
    for src_rel, dst_rel in IMAGE_MAP.items():
        new_image = edit_image(src_rel, dst_rel)
        make_pdf(new_image)
        rebuilt.append(new_image)

    # Remove superseded v2 WebPs after successful creation.
    for src_rel in IMAGE_MAP:
        (EXAMPLES / src_rel).unlink()

    remove_old_visual_pdfs()
    rebuild_logos()
    update_html()
    print(f"Rebuilt {len(rebuilt)} WebP assets and matching PDFs.")
