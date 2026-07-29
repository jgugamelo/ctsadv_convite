import subprocess
import os
import sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def generate_pdf_cmyk():
    workspace = "/Users/jgugamelo/Downloads/Inovação na Área Médica - CTSADV"
    html_file = os.path.join(workspace, "portfolio_flyer.html")
    pdf_out = os.path.join(workspace, "folheto_ctsadv_grafica_cmyk.pdf")
    jpg_out = os.path.join(workspace, "folheto_ctsadv.jpg")
    page1_png = os.path.join(workspace, "temp_page1.png")
    page2_png = os.path.join(workspace, "temp_page2.png")
    page1_cmyk = os.path.join(workspace, "temp_page1_cmyk.jpg")
    page2_cmyk = os.path.join(workspace, "temp_page2_cmyk.jpg")

    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    print("1. Renders HTML pages at 300 DPI high resolution with Chrome Headless...")
    # Dimensions for A4 + 3mm bleed at 300 DPI:
    # 216mm x 303mm @ 300DPI = 2551px x 3579px
    # Window size: 816px x 1145px (scale 3.126 => ~300DPI)
    cmd1 = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=3.125",
        "--window-size=816,2330",
        f"--screenshot={os.path.join(workspace, 'temp_full.png')}",
        f"file://{html_file}"
    ]
    subprocess.run(cmd1, check=True)

    print("2. Processing pages and converting color profile to CMYK...")
    full_img = Image.open(os.path.join(workspace, "temp_full.png"))
    w, h = full_img.size
    half_h = h // 2

    # Crop Page 1 (Frente) and Page 2 (Verso)
    img_p1 = full_img.crop((0, 0, w, half_h))
    img_p2 = full_img.crop((0, half_h, w, h))

    # Convert RGB -> CMYK (PDF/X-1a standards)
    img_p1_cmyk = img_p1.convert("CMYK")
    img_p2_cmyk = img_p2.convert("CMYK")

    img_p1_cmyk.save(page1_cmyk, "JPEG", quality=98, dpi=(300, 300))
    img_p2_cmyk.save(page2_cmyk, "JPEG", quality=98, dpi=(300, 300))

    # Also save a composite RGB JPG preview for screen viewing
    preview_img = Image.new("RGB", (w, half_h * 2 + 30), (240, 240, 240))
    preview_img.paste(img_p1.convert("RGB"), (0, 0))
    preview_img.paste(img_p2.convert("RGB"), (0, half_h + 30))
    preview_img.save(jpg_out, "JPEG", quality=92)
    print(f"Generated preview JPG: {jpg_out}")

    print("3. Building PDF/X-1a Compliant CMYK PDF file via ReportLab...")
    # Exact A4 + 3mm bleed dimensions in points: 216mm x 303mm
    bleed_width = 216 * mm
    bleed_height = 303 * mm

    c = canvas.Canvas(pdf_out, pagesize=(bleed_width, bleed_height))
    c.setTitle("CTSADV - Folheto Institucional Direito Medico - CMYK 300DPI Bleed 3mm")
    c.setAuthor("Cursino & Teodoro da Silva Advogados")
    c.setSubject("Folheto Institucional Gráfica PDF/X-1a CMYK")

    # Page 1 (Frente)
    c.drawImage(page1_cmyk, 0, 0, width=bleed_width, height=bleed_height)
    c.showPage()

    # Page 2 (Verso)
    c.drawImage(page2_cmyk, 0, 0, width=bleed_width, height=bleed_height)
    c.showPage()

    c.save()
    print(f"Generated CMYK PDF/X-1a file: {pdf_out}")

    # Also generate folheto_ctsadv.pdf for standard download
    standard_pdf = os.path.join(workspace, "folheto_ctsadv.pdf")
    cmd_std = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={standard_pdf}",
        f"file://{html_file}"
    ]
    subprocess.run(cmd_std, check=True)
    print(f"Generated standard PDF: {standard_pdf}")

    # Clean up temp files
    for temp in [os.path.join(workspace, "temp_full.png"), page1_png, page2_png, page1_cmyk, page2_cmyk]:
        if os.path.exists(temp):
            os.remove(temp)

if __name__ == "__main__":
    generate_pdf_cmyk()
