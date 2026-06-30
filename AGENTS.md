# AGENTS.md

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

## Design history store

`knowledge_base/history_store.py` persists every analysis (thumbnail + serialized
`DesignReport` + CLIP embedding) behind a `HistoryStore` Protocol with **two backends**,
chosen by `get_history_store()`:
- `QdrantHistoryStore` — used when `QDRANT_URL` is set (the deployment backend, Qdrant Cloud
  free tier). Thumbnail stored inline as base64 in the point payload.
- `LanceDBHistoryStore` — local on-disk fallback (`history/`) when `QDRANT_URL` is unset.

**All backend-specific code is isolated here**; callers (`app.py`) only use `save_design` /
`search_designs` / `list_recent`. Config: `QDRANT_URL`, `QDRANT_API_KEY`,
`QDRANT_HISTORY_COLLECTION` in `config/settings.py`. Possible future swap: another vector DB —
just add a new class implementing the Protocol.

## Conventions

- Reference image filenames are `{category}_{slug}.png`; `ingest.py` derives category +
  caption from the name. Keep that scheme when adding sources.
- CLIP is cross-modal, so text→image search works against `design_images`.
- Keep the UI calm: use `score_color()` for scores; avoid decorative `:green[]`/
  `:orange[]`/`:violet[]` Streamlit color markup (severity colors in the UX detail
  expander are intentional/semantic).
- Adding an agent: see the steps in `README.md` ("Adding A New Agent").

## Project state & deployment (context handoff, 2026-06-14)

**Deployed and live:** Hugging Face Space `ananthmohan/Product_Design_Evaluator` —
**private**, **Docker** SDK, free `cpu-basic`. The `Dockerfile` installs CPU torch + deps and
runs `streamlit run app.py` on port 8501. History → Qdrant Cloud free cluster (secrets set in
the Space: `OPENROUTER_API_KEY`, `TAVILY_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`).

**Git:** local repo only, branch `main`, remote `space` → the HF Space. **No GitHub remote**
(user asked to hold). Uses **Git LFS** for `*.png` and `knowledge_base/lancedb_data/**`
(HF rejects plain-git binaries). `.env`, `history/`, `.Codex/` are gitignored.

**Deploy gotchas already solved (keep these):**
- File uploads broke inside HF's cross-origin iframe → fixed by `enableCORS=false` +
  `enableXsrfProtection=false` in `.streamlit/config.toml`. Do not re-enable.
- Reference images showed "image not found" because the index stored absolute build-machine
  paths → `retrieval/retriever._resolve_ref_path()` now resolves them by filename against
  `REFERENCE_IMAGES_DIR`. Keep reference images addressable by basename.
- `README.md` YAML frontmatter drives the Space (sdk: docker, app_port: 8501,
  `short_description` must be ≤60 chars).
- thum.io renders async; use the `wait/…/maxAge/1` options in `scraper.py` to avoid the
  "loading" placeholder. Verify scraped shots visually (e.g. Warby Parker was a maintenance
  page → replaced with Glossier).

**Uncommitted local work being held (per user "hold on git"):** refreshed all 25 reference
screenshots and swapped Warby Parker → Glossier, with the LanceDB index rebuilt. NOT yet
committed/pushed, so the **live Space still shows the older thumbnails**. To ship it later:
`git add -A && git commit && git push space main`, then the Space rebuilds (~few min).

**To redeploy after changes:** push to `space main`; poll status with
`python -c "from huggingface_hub import HfApi; print(HfApi().get_space_runtime('ananthmohan/Product_Design_Evaluator').stage)"`
until `RUNNING`.
