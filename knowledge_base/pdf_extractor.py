import fitz
from pathlib import Path
from PIL import Image
import io


def extract_from_pdf(pdf_path: str, output_image_dir: str) -> tuple[list[dict], list[dict]]:
    """Extract text blocks and images from a PDF. Returns (text_chunks, image_records)."""
    doc = fitz.open(pdf_path)
    source_name = Path(pdf_path).stem
    Path(output_image_dir).mkdir(parents=True, exist_ok=True)

    text_chunks = []
    image_records = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        page_text = page.get_text("text").strip()
        if page_text:
            text_chunks.append({
                "text": page_text,
                "source": source_name,
                "section": f"page_{page_num + 1}",
                "page": page_num + 1,
            })

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n > 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                img_filename = f"{source_name}_p{page_num + 1}_img{img_index}.png"
                img_path = str(Path(output_image_dir) / img_filename)
                pix.save(img_path)

                image_records.append({
                    "image_path": img_path,
                    "source": source_name,
                    "category": "pdf_illustration",
                    "caption": f"Image from {source_name}, page {page_num + 1}",
                    "page": page_num + 1,
                })
            except Exception:
                continue

    doc.close()
    return text_chunks, image_records
