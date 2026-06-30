from collections.abc import Callable, Sequence
from typing import Any


def load_history_records(
    store_factory: Callable[[], Any],
    query: str | None,
    recent_limit: int = 24,
    search_limit: int = 12,
) -> tuple[list[Any], str | None]:
    """Load history records without letting backend errors break the tab."""
    try:
        store = store_factory()
        normalized_query = (query or "").strip()
        if normalized_query:
            return (
                store.search_designs(query_text=normalized_query, limit=search_limit),
                None,
            )
        return store.list_recent(limit=recent_limit), None
    except Exception as exc:
        return [], f"Could not load past designs: {exc}"


def find_history_record(records: Sequence[Any], selected_id: str | None) -> Any | None:
    if not selected_id:
        return None
    return next((record for record in records if record.id == selected_id), None)
