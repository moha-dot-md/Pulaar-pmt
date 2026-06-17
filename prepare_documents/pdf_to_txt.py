from pdf2image import convert_from_path
import pytesseract
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
PDF_DIR = Path("pdfs")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

POPPLER_PATH = r"C:\Users\PC-TCM\Documents\poppler-25.12.0\Library\bin"
TESSERACT_PATH = r"C:\Users\PC-TCM\AppData\Local\Programming and engineering\tesseract\tesseract.exe"

# Tell pytesseract explicitly where Tesseract is
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# OCR language fallback for Pulaar
OCR_LANG = "swa"

# -----------------------------
# PROCESS PDFs
# -----------------------------
for pdf_file in PDF_DIR.glob("*.pdf"):
    print(f"Processing: {pdf_file.name}")

    pages = convert_from_path(pdf_file, dpi=300, poppler_path=POPPLER_PATH)

    full_text = []

    for i, page in enumerate(pages, start=1):
        print(f"  OCR page {i}")
        page_text = pytesseract.image_to_string(page, lang=OCR_LANG, config="--psm 3")
        full_text.append(page_text)

    out_file = OUTPUT_DIR / f"{pdf_file.stem}.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(full_text))

    print(f"Saved → {out_file}\n")

print("All PDFs processed.")
