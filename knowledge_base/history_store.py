"""Persistent, shared history of every analyzed design.

Every analysis is saved here so anyone can browse and learn from past evaluations.
The store is hidden behind a small `HistoryStore` interface with two backends:

- `QdrantHistoryStore` — used when `QDRANT_URL` is set (Qdrant Cloud free tier). This is
  the deployment backend: persistent and shared across the hosted app and any local runs
  that point at the same cluster. Thumbnails are stored inline as base64 in the payload.
- `LanceDBHistoryStore` — local on-disk fallback used when `QDRANT_URL` is unset.

Callers only ever touch `get_history_store()` and the interface methods, so swapping or
choosing a backend requires no changes outside this module.
"""
from __future__ import annotations

import base64
import io
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Protocol

import lancedb
from PIL import Image

from config.settings import BASE_DIR, EMBEDDING_DIM
from knowledge_base.embedder import embed_image, embed_text
from models.schemas import DesignReport, HistoryRecord

HISTORY_DIR = Path(BASE_DIR) / "history"
HISTORY_IMAGES_DIR = HISTORY_DIR / "images"
HISTORY_DB_PATH = str(HISTORY_DIR / "lancedb_data")
HISTORY_TABLE = "design_history"
THUMB_SIZE = (480, 480)


class HistoryStore(Protocol):
    """Backend-agnostic contract for the shared design history."""

    def save_design(self, image: Image.Image, report: DesignReport, model: str) -> str: ...

    def search_designs(
        self,
        query_text: Optional[str] = None,
        query_image: Optional[Image.Image] = None,
        limit: int = 12,
    ) -> list[HistoryRecord]: ...

    def list_recent(self, limit: int = 24) -> list[HistoryRecord]: ...


def _summary_of(report: DesignReport) -> str:
    if report.synthesis and report.synthesis.executive_summary:
        return report.synthesis.executive_summary
    return ""


def _score_of(report: DesignReport) -> int:
    if report.synthesis:
        return int(report.synthesis.overall_score)
    return 0


def _category_of(report: DesignReport) -> str:
    if report.market_research and report.market_research.design_category:
        return report.market_research.design_category
    return "general"


def _row_to_record(row: dict) -> HistoryRecord:
    report = None
    raw = row.get("report_json")
    if raw:
        try:
            report = DesignReport(**json.loads(raw))
        except Exception:
            report = None
    return HistoryRecord(
        id=row["id"],
        timestamp=row.get("timestamp", ""),
        model=row.get("model", ""),
        overall_score=int(row.get("overall_score", 0)),
        summary=row.get("summary", ""),
        category=row.get("category", ""),
        thumb_path=row.get("thumb_path", ""),
        report=report,
        score=float(row.get("_distance", 0.0)),
    )


class LanceDBHistoryStore:
    """LanceDB-backed implementation. All DB-specific code lives here."""

    def __init__(self) -> None:
        HISTORY_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        self._db = lancedb.connect(HISTORY_DB_PATH)

    def _table(self):
        if HISTORY_TABLE in self._db.table_names():
            return self._db.open_table(HISTORY_TABLE)
        return None

    def save_design(self, image: Image.Image, report: DesignReport, model: str) -> str:
        record_id = uuid.uuid4().hex[:12]

        thumb = image.convert("RGB").copy()
        thumb.thumbnail(THUMB_SIZE)
        thumb_path = HISTORY_IMAGES_DIR / f"{record_id}.png"
        thumb.save(thumb_path)

        vector = embed_image(image.convert("RGB"))
        row = {
            "id": record_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "overall_score": _score_of(report),
            "summary": _summary_of(report),
            "category": _category_of(report),
            "thumb_path": str(thumb_path),
            "report_json": report.model_dump_json(),
            "vector": vector,
        }

        table = self._table()
        if table is None:
            self._db.create_table(HISTORY_TABLE, data=[row])
        else:
            table.add([row])
        return record_id

    def search_designs(
        self,
        query_text: Optional[str] = None,
        query_image: Optional[Image.Image] = None,
        limit: int = 12,
    ) -> list[HistoryRecord]:
        table = self._table()
        if table is None:
            return []
        if query_image is not None:
            query_vector = embed_image(query_image.convert("RGB"))
        elif query_text:
            query_vector = embed_text(query_text)
        else:
            return self.list_recent(limit)
        rows = table.search(query_vector).limit(limit).to_list()
        return [_row_to_record(r) for r in rows]

    def list_recent(self, limit: int = 24) -> list[HistoryRecord]:
        table = self._table()
        if table is None:
            return []
        rows = table.to_pandas().to_dict("records")
        rows.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
        return [_row_to_record(r) for r in rows[:limit]]


def _thumb_to_b64(image: Image.Image) -> str:
    thumb = image.convert("RGB").copy()
    thumb.thumbnail(THUMB_SIZE)
    buf = io.BytesIO()
    thumb.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


class QdrantHistoryStore:
    """Qdrant-backed implementation. All Qdrant-specific code lives here."""

    def __init__(self) -> None:
        from qdrant_client import QdrantClient

        from config.settings import (
            QDRANT_API_KEY,
            QDRANT_HISTORY_COLLECTION,
            QDRANT_URL,
        )

        self._collection = QDRANT_HISTORY_COLLECTION
        self._client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY or None)
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        from qdrant_client.models import Distance, VectorParams

        existing = {c.name for c in self._client.get_collections().collections}
        if self._collection not in existing:
            self._client.create_collection(
                collection_name=self._collection,
                vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
            )

    def _point_to_record(self, point) -> HistoryRecord:
        payload = point.payload or {}
        report = None
        raw = payload.get("report_json")
        if raw:
            try:
                report = DesignReport(**json.loads(raw))
            except Exception:
                report = None
        return HistoryRecord(
            id=str(point.id),
            timestamp=payload.get("timestamp", ""),
            model=payload.get("model", ""),
            overall_score=int(payload.get("overall_score", 0)),
            summary=payload.get("summary", ""),
            category=payload.get("category", ""),
            thumb_b64=payload.get("thumb_b64", ""),
            report=report,
            score=float(getattr(point, "score", 0.0) or 0.0),
        )

    def save_design(self, image: Image.Image, report: DesignReport, model: str) -> str:
        from qdrant_client.models import PointStruct

        point_id = str(uuid.uuid4())
        vector = embed_image(image.convert("RGB"))
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "overall_score": _score_of(report),
            "summary": _summary_of(report),
            "category": _category_of(report),
            "report_json": report.model_dump_json(),
            "thumb_b64": _thumb_to_b64(image),
        }
        self._client.upsert(
            collection_name=self._collection,
            points=[PointStruct(id=point_id, vector=vector, payload=payload)],
        )
        return point_id

    def search_designs(
        self,
        query_text: Optional[str] = None,
        query_image: Optional[Image.Image] = None,
        limit: int = 12,
    ) -> list[HistoryRecord]:
        if query_image is not None:
            query_vector = embed_image(query_image.convert("RGB"))
        elif query_text:
            query_vector = embed_text(query_text)
        else:
            return self.list_recent(limit)
        result = self._client.query_points(
            collection_name=self._collection,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )
        return [self._point_to_record(p) for p in result.points]

    def list_recent(self, limit: int = 24) -> list[HistoryRecord]:
        points, _ = self._client.scroll(
            collection_name=self._collection,
            limit=256,
            with_payload=True,
        )
        records = [self._point_to_record(p) for p in points]
        records.sort(key=lambda r: r.timestamp, reverse=True)
        return records[:limit]


_store: Optional[HistoryStore] = None


def get_history_store() -> HistoryStore:
    """Return the process-wide history store.

    Uses Qdrant when ``QDRANT_URL`` is configured (the deployment backend); otherwise
    falls back to the local on-disk LanceDB store.
    """
    global _store
    if _store is None:
        from config.settings import QDRANT_URL

        _store = QdrantHistoryStore() if QDRANT_URL else LanceDBHistoryStore()
    return _store
