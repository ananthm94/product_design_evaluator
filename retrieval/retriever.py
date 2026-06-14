import os

import lancedb
from PIL import Image

from config.settings import LANCEDB_PATH, TEXT_TOP_K, IMAGE_TOP_K, REFERENCE_IMAGES_DIR
from knowledge_base.embedder import embed_image, embed_text
from models.schemas import RetrievalContext, RetrievedTextChunk, RetrievedImage


def _resolve_ref_path(stored_path: str) -> str:
    """Reference images are addressed by filename so paths stay portable.

    The LanceDB index may have been built on another machine (absolute paths),
    so resolve each image against the current reference-images directory.
    """
    candidate = os.path.join(REFERENCE_IMAGES_DIR, os.path.basename(stored_path))
    return candidate if os.path.exists(candidate) else stored_path


def _row_to_image(row: dict) -> RetrievedImage:
    return RetrievedImage(
        image_path=_resolve_ref_path(row["image_path"]),
        source=row["source"],
        category=row.get("category", ""),
        caption=row.get("caption", ""),
        score=float(row.get("_distance", 0)),
    )


def search_reference_images(query_text: str, limit: int = IMAGE_TOP_K) -> list[RetrievedImage]:
    """Text→image search over the reference-design library (CLIP is cross-modal)."""
    db = lancedb.connect(LANCEDB_PATH)
    if "design_images" not in db.table_names():
        return []
    query_vector = embed_text(query_text)
    rows = db.open_table("design_images").search(query_vector).limit(limit).to_list()
    return [_row_to_image(r) for r in rows]


def list_reference_images(limit: int = 60) -> list[RetrievedImage]:
    """Return all reference images for browse-all in the library tab."""
    db = lancedb.connect(LANCEDB_PATH)
    if "design_images" not in db.table_names():
        return []
    rows = db.open_table("design_images").to_pandas().to_dict("records")
    return [_row_to_image(r) for r in rows[:limit]]


def retrieve_context(image: Image.Image) -> RetrievalContext:
    """Query LanceDB with an uploaded image to find similar reference designs and relevant text guidelines."""
    query_vector = embed_image(image)
    db = lancedb.connect(LANCEDB_PATH)

    relevant_guidelines = []
    similar_images = []

    # Query text guidelines (image→text cross-modal retrieval)
    if "design_text" in db.table_names():
        text_table = db.open_table("design_text")
        text_results = text_table.search(query_vector).limit(TEXT_TOP_K).to_list()

        for row in text_results:
            relevant_guidelines.append(RetrievedTextChunk(
                text=row["text"],
                source=row["source"],
                section=row.get("section", ""),
                score=float(row.get("_distance", 0)),
            ))

    # Query reference images (image→image retrieval)
    if "design_images" in db.table_names():
        image_table = db.open_table("design_images")
        image_results = image_table.search(query_vector).limit(IMAGE_TOP_K).to_list()

        for row in image_results:
            similar_images.append(_row_to_image(row))

    return RetrievalContext(
        relevant_guidelines=relevant_guidelines,
        similar_images=similar_images,
    )
