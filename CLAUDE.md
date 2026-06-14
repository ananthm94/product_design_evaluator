# CLAUDE.md

Guidance for working in this repository.

## What this is

Multimodal AI Design Analysis Suite — a Streamlit app that critiques an uploaded
product/app screenshot. It combines CLIP-based image RAG (LanceDB), a LangGraph
multi-agent flow, and Tavily live web research, then synthesizes an executive report.
It also keeps a shared, searchable memory of every analyzed design.

## Run / build commands

```bash
streamlit run app.py                       # launch the app (config in .streamlit/config.toml)
python knowledge_base/scraper.py           # scrape reference site screenshots + rebuild index
python knowledge_base/scraper.py --no-ingest   # download screenshots only
python knowledge_base/ingest.py            # rebuild the LanceDB knowledge base from sources/
```

Keys live in `.env` (`OPENROUTER_API_KEY` required; `TAVILY_API_KEY`,
`LANGSMITH_API_KEY` optional) and can also be entered in the sidebar.

Quick checks:

```bash
python -m py_compile app.py retrieval/retriever.py knowledge_base/scraper.py \
  knowledge_base/history_store.py ui/components.py ui/report_renderer.py models/schemas.py
python -c "from agents.graph import build_graph; build_graph(['visual','ux','market','live_research']); print('graph ok')"
```

## Architecture

- `app.py` — Streamlit entrypoint. Three tabs: **Analyze** (upload + inline agent
  toggles + streamed analysis), **Reference Library** (search scraped reference
  screenshots), **Past Designs** (search the shared design history). Sidebar holds API
  keys + model. Analysis runs via `graph.stream(..., stream_mode="updates")` so each
  LangGraph node is shown live (see `NODE_LABELS`).
- `agents/graph.py` — builds the LangGraph: `START → retrieve → {visual, ux, market,
  live_research} → synthesize → END`. Only enabled agents are added as nodes.
- `agents/*.py` — specialist agents (visual, ux, market, live_research) + synthesizer.
  Each LLM agent calls OpenRouter via `ChatOpenAI`, sends the base64 screenshot +
  retrieved guidelines, returns a Pydantic result, and degrades gracefully on failure.
- `retrieval/retriever.py` — `retrieve_context(image)` for analysis;
  `search_reference_images(text)` / `list_reference_images()` for the library tab.
- `knowledge_base/` — `embedder.py` (CLIP via open-clip), `ingest.py` (markdown/PDF/
  image → LanceDB tables `design_text`, `design_images`), `scraper.py` (thum.io
  screenshots of curated sites → `sources/reference_images/`), `history_store.py`.
- `ui/` — `report_renderer.py` (report cards, detail dialogs) and `components.py`
  (score pills via `score_color`, reference gallery).
- `models/schemas.py` — all Pydantic contracts (results, `DesignReport`, `GraphState`,
  `HistoryRecord`).
- `config/settings.py` — paths, CLIP/model settings, retrieval limits.

## Design history store (note for future work)

`knowledge_base/history_store.py` persists every analysis (thumbnail + serialized
`DesignReport` + CLIP embedding) to a LanceDB table `design_history` under `history/`.
It is deliberately behind a `HistoryStore` Protocol with a `LanceDBHistoryStore`
implementation and a `get_history_store()` singleton — **all backend-specific code is
isolated here**. The intent is to swap the backend to **Qdrant** later without touching
callers (`app.py` only uses `save_design` / `search_designs` / `list_recent`).

## Conventions

- Reference image filenames are `{category}_{slug}.png`; `ingest.py` derives category +
  caption from the name. Keep that scheme when adding sources.
- CLIP is cross-modal, so text→image search works against `design_images`.
- Keep the UI calm: use `score_color()` for scores; avoid decorative `:green[]`/
  `:orange[]`/`:violet[]` Streamlit color markup (severity colors in the UX detail
  expander are intentional/semantic).
- Adding an agent: see the steps in `README.md` ("Adding A New Agent").
