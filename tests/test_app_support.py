from dataclasses import dataclass


def test_effective_secret_prefers_typed_value(monkeypatch):
    from utils.secret_inputs import effective_secret

    monkeypatch.setenv("OPENROUTER_API_KEY", "server-secret")

    assert effective_secret(" typed-secret ", "OPENROUTER_API_KEY") == "typed-secret"


def test_effective_secret_falls_back_to_env_without_exposing_default(monkeypatch):
    from utils.secret_inputs import effective_secret

    monkeypatch.setenv("OPENROUTER_API_KEY", "server-secret")

    assert effective_secret("", "OPENROUTER_API_KEY") == "server-secret"
    assert effective_secret(None, "OPENROUTER_API_KEY") == "server-secret"


def test_load_history_records_returns_recent_records_when_query_is_empty():
    from ui.history_helpers import load_history_records

    records, error = load_history_records(lambda: FakeHistoryStore(), "")

    assert error is None
    assert [record.id for record in records] == ["recent-1"]


def test_load_history_records_returns_search_records_when_query_is_present():
    from ui.history_helpers import load_history_records

    records, error = load_history_records(lambda: FakeHistoryStore(), " fintech ")

    assert error is None
    assert [record.id for record in records] == ["search-1"]


def test_load_history_records_contains_backend_errors():
    from ui.history_helpers import load_history_records

    records, error = load_history_records(FailingHistoryStore, "")

    assert records == []
    assert error == "Could not load past designs: qdrant unavailable"


def test_find_history_record_matches_selected_id():
    from ui.history_helpers import find_history_record

    records = [FakeRecord("first"), FakeRecord("second")]

    assert find_history_record(records, "second").id == "second"
    assert find_history_record(records, "missing") is None
    assert find_history_record(records, None) is None


@dataclass
class FakeRecord:
    id: str


class FakeHistoryStore:
    def list_recent(self, limit):
        assert limit == 24
        return [FakeRecord("recent-1")]

    def search_designs(self, query_text, limit):
        assert query_text == "fintech"
        assert limit == 12
        return [FakeRecord("search-1")]


def FailingHistoryStore():
    raise RuntimeError("qdrant unavailable")
