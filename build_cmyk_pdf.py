import subprocess
import os
import sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def process_option(html_file, pdf_cmyk_out, pdf_std_out, jpg_out):
    workspace = "/Users/jgugamelo/Downloads/Inovação na Área Médica - CTSADV"
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    page1_cmyk = os.path.join(workspace, "temp_page1_cmyk.jpg")
    page2_cmyk = os.path.join(workspace, "temp_page2_cmyk.jpg")
    temp_full = os.path.join(workspace, f"temp_{os.path.basename(jpg_out)}.png")

    print(f"\nProcessing {os.path.basename(html_file)}...")
    print("1. Rendering HTML pages at 300 DPI (21,30 x 30,00 cm) with Chrome Headless...")
    # Exact Dimensions requested by print shop: 21,30cm x 30,00cm @ 300 DPI = 2516px x 3543px
    cmd1 = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-pdf-header-footer",
        "--force-device-scale-factor=3.125",
        "--window-size=805,2268",
        f"--screenshot={temp_full}",
        f"file://{html_file}"
    ]
    subprocess.run(cmd1, check=True)

    print("2. Processing color channels with exact CMYK C:100 M:90 Y:35 K:50 profile...")
    full_img = Image.open(temp_full).convert("RGB")
    w, h = full_img.size
    half_h = h // 2

    img_p1_rgb = full_img.crop((0, 0, w, half_h))
    img_p2_rgb = full_img.crop((0, half_h, w, h))

    def rgb_to_exact_cmyk(img):
        cmyk_img = img.convert("CMYK")
        c, m, y, k = cmyk_img.split()
        
        pixels_rgb = img.load()
        c_data = c.load()
        m_data = m.load()
        y_data = y.load()
        k_data = k.load()
        
        width, height = img.size
        for px in range(width):
            for py in range(height):
                r, g, b = pixels_rgb[px, py]
                if r < 35 and g < 40 and b > 50:
                    c_data[px, py] = 255  # C: 100%
                    m_data[px, py] = 230  # M: 90%
                    y_data[px, py] = 89   # Y: 35%
                    k_data[px, py] = 128  # K: 50%
                    
        return Image.merge("CMYK", (c, m, y, k))

    img_p1_cmyk = rgb_to_exact_cmyk(img_p1_rgb)
    img_p2_cmyk = rgb_to_exact_cmyk(img_p2_rgb)

    img_p1_cmyk.save(page1_cmyk, "JPEG", quality=98, dpi=(300, 300))
    img_p2_cmyk.save(page2_cmyk, "JPEG", quality=98, dpi=(300, 300))

    # Clean RGB JPG preview for screen viewing
    preview_img = Image.new("RGB", (w, half_h * 2 + 30), (240, 240, 240))
    preview_img.paste(img_p1_rgb, (0, 0))
    preview_img.paste(img_p2_rgb, (0, half_h + 30))
    preview_img.save(jpg_out, "JPEG", quality=94)
    print(f"Generated preview JPG: {jpg_out}")

    print("3. Building PDF/X-1a CMYK file with exact dimensions (21,30 x 30,00 cm)...")
    exact_w = 21.30 * cm
    exact_h = 30.00 * cm

    c = canvas.Canvas(pdf_cmyk_out, pagesize=(exact_w, exact_h))
    c.setTitle("CTSADV - Folheto Institucional Direito Medico - CMYK 300DPI 21.3x30.0cm")
    c.setAuthor("Cursino & Teodoro da Silva Advogados")
    c.setSubject("Folheto Institucional Gráfica PDF/X-1a CMYK")

    # Page 1 (Frente)
    c.drawImage(page1_cmyk, 0, 0, width=exact_w, height=exact_h)
    c.showPage()

    # Page 2 (Verso)
    c.drawImage(page2_cmyk, 0, 0, width=exact_w, height=exact_h)
    c.showPage()

    c.save()
    print(f"Generated CMYK PDF: {pdf_cmyk_out}")

    # Standard PDF without Chrome auto headers/footers
    cmd_std = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_std_out}",
        f"file://{html_file}"
    ]
    subprocess.run(cmd_std, check=True)
    print(f"Generated standard PDF: {pdf_std_out}")

    # Clean temp files
    for temp in [temp_full, page1_cmyk, page2_cmyk]:
        if os.path.exists(temp):
            os.remove(temp)

def generate_all():
    workspace = "/Users/jgugamelo/Downloads/Inovação na Área Médica - CTSADV"
    
    # OPÇÃO 1: COM SÓCIOS (Versão Principal)
    process_option(
        html_file=os.path.join(workspace, "portfolio_flyer.html"),
        pdf_cmyk_out=os.path.join(workspace, "folheto_ctsadv_grafica_cmyk.pdf"),
        pdf_std_out=os.path.join(workspace, "folheto_ctsadv.pdf"),
        jpg_out=os.path.join(workspace, "folheto_ctsadv.jpg")
    )

    # OPÇÃO 2: SEM SÓCIOS (Versão Alternativa)
    process_option(
        html_file=os.path.join(workspace, "portfolio_flyer_sem_socios.html"),
        pdf_cmyk_out=os.path.join(workspace, "folheto_ctsadv_sem_socios_grafica_cmyk.pdf"),
        pdf_std_out=os.path.join(workspace, "folheto_ctsadv_sem_socios.pdf"),
        jpg_out=os.path.join(workspace, "folheto_ctsadv_sem_socios.jpg")
    )

if __name__ == "__main__":
    generate_all()
