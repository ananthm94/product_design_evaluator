import os
import json
from pathlib import Path
from PIL import Image
import lancedb
import pyarrow as pa
import numpy as np

from config.settings import (
    LANCEDB_PATH, SOURCES_DIR, REFERENCE_IMAGES_DIR,
    TEXT_CHUNK_SIZE, TEXT_CHUNK_OVERLAP, EMBEDDING_DIM,
)
from knowledge_base.embedder import embed_text, embed_texts, embed_image, embed_images
from knowledge_base.pdf_extractor import extract_from_pdf


def chunk_text(text: str, source: str, section: str = "", chunk_size: int = TEXT_CHUNK_SIZE, overlap: int = TEXT_CHUNK_OVERLAP) -> list[dict]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        if len(chunk_text.strip()) > 20:
            chunks.append({
                "text": chunk_text,
                "source": source,
                "section": section,
            })
        start += chunk_size - overlap
    return chunks


def parse_markdown_sections(filepath: str) -> list[dict]:
    source = Path(filepath).stem
    with open(filepath, "r") as f:
        content = f.read()

    sections = []
    current_section = ""
    current_text = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_text and current_section:
                sections.append({
                    "text": "\n".join(current_text),
                    "source": source,
                    "section": current_section,
                })
            current_section = line.lstrip("#").strip()
            current_text = [line]
        else:
            current_text.append(line)

    if current_text and current_section:
        sections.append({
            "text": "\n".join(current_text),
            "source": source,
            "section": current_section,
        })

    all_chunks = []
    for sec in sections:
        all_chunks.extend(chunk_text(sec["text"], sec["source"], sec["section"]))

    return all_chunks


def ingest_knowledge_base():
    """Full ingestion pipeline: read sources → chunk → embed → store in LanceDB."""
    db = lancedb.connect(LANCEDB_PATH)

    all_text_chunks = []
    all_image_records = []

    # 1. Ingest markdown files
    sources_path = Path(SOURCES_DIR)
    for md_file in sources_path.glob("*.md"):
        print(f"Processing markdown: {md_file.name}")
        chunks = parse_markdown_sections(str(md_file))
        all_text_chunks.extend(chunks)

    # 2. Ingest PDFs
    for pdf_file in sources_path.glob("*.pdf"):
        print(f"Processing PDF: {pdf_file.name}")
        processed_dir = str(sources_path / "processed_images")
        text_chunks, image_records = extract_from_pdf(str(pdf_file), processed_dir)
        for tc in text_chunks:
            all_text_chunks.extend(chunk_text(tc["text"], tc["source"], tc["section"]))
        all_image_records.extend(image_records)

    # 3. Ingest reference images
    ref_dir = Path(REFERENCE_IMAGES_DIR)
    if ref_dir.exists():
        for img_file in ref_dir.glob("*"):
            if img_file.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                all_image_records.append({
                    "image_path": str(img_file),
                    "source": "reference_collection",
                    "category": img_file.stem.split("_")[0] if "_" in img_file.stem else "general",
                    "caption": img_file.stem.replace("_", " ").replace("-", " "),
                })

    # 4. Embed text chunks
    if all_text_chunks:
        print(f"Embedding {len(all_text_chunks)} text chunks...")
        texts = [c["text"][:300] for c in all_text_chunks]  # CLIP has 77 token limit, truncate
        batch_size = 32
        all_text_vectors = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            all_text_vectors.extend(embed_texts(batch))

        text_data = []
        for i, chunk in enumerate(all_text_chunks):
            text_data.append({
                "id": f"text_{i}",
                "text": chunk["text"],
                "source": chunk["source"],
                "section": chunk["section"],
                "vector": all_text_vectors[i],
            })

        if "design_text" in db.table_names():
            db.drop_table("design_text")
        db.create_table("design_text", data=text_data)
        print(f"Stored {len(text_data)} text chunks in LanceDB")

    # 5. Embed images
    if all_image_records:
        print(f"Embedding {len(all_image_records)} images...")
        images = []
        valid_records = []
        for rec in all_image_records:
            try:
                img = Image.open(rec["image_path"]).convert("RGB")
                img = img.resize((224, 224))
                images.append(img)
                valid_records.append(rec)
            except Exception as e:
                print(f"  Skipping {rec['image_path']}: {e}")

        if images:
            batch_size = 16
            all_image_vectors = []
            for i in range(0, len(images), batch_size):
                batch = images[i:i + batch_size]
                all_image_vectors.extend(embed_images(batch))

            image_data = []
            for i, rec in enumerate(valid_records):
                image_data.append({
                    "id": f"img_{i}",
                    "image_path": rec["image_path"],
                    "source": rec["source"],
                    "category": rec["category"],
                    "caption": rec.get("caption", ""),
                    "vector": all_image_vectors[i],
                })

            if "design_images" in db.table_names():
                db.drop_table("design_images")
            db.create_table("design_images", data=image_data)
            print(f"Stored {len(image_data)} images in LanceDB")

    print("Knowledge base ingestion complete!")
    return {
        "text_chunks": len(all_text_chunks),
        "images": len(all_image_records),
    }


def is_knowledge_base_ready() -> bool:
    try:
        db = lancedb.connect(LANCEDB_PATH)
        return "design_text" in db.table_names()
    except Exception:
        return False


if __name__ == "__main__":
    ingest_knowledge_base()
