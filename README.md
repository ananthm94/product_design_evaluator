---
title: Product Design Evaluator
emoji: 🎨
colorFrom: blue
colorTo: red
sdk: streamlit
app_file: app.py
pinned: false
---

## Product Design Evaluator

## AI multi-agent design critique with image RAG

[[Try the Live Demo on Hugging Face Spaces](http://huggingface.co/spaces/ananthmohan/Product_Design_Evaluator)]

Multimodal AI Design Analysis Suite is a Streamlit app for reviewing product and app screenshots. It combines image-based retrieval, design knowledge sources, and multiple specialist LLM agents to produce a structured design critique.

The app flow is:

1. Upload a design screenshot.
2. Choose which analysis agents to run.
3. Retrieve relevant design guidelines from the local LanceDB knowledge base.
4. Optionally run Tavily-powered live web research for current market/design context.
5. Run selected specialist agents against the screenshot and retrieved context.
6. Synthesize the agent outputs into an executive report.
7. Render scores, findings, recommendations, priority actions, sources, and detail dialogs in the UI.

## Architecture

```text
app.py
  Streamlit entrypoint and user flow orchestration

models/
  Pydantic schemas shared across agents, graph state, retrieval, and UI

agents/
  LangGraph workflow, specialist LLM agents, and live Tavily research

retrieval/
  LanceDB lookup for relevant text guidelines and reference images

knowledge_base/
  Source documents, ingestion pipeline, CLIP embeddings, and LanceDB data

ui/
  Streamlit report cards, detail dialogs, reference gallery, and display helpers

utils/
  Image conversion/resizing and LLM utility helpers

config/
  Paths, model options, retrieval limits, and runtime constants
```

## Runtime Flow

### 1. Streamlit UI

[app.py](app.py) owns the user-facing workflow:

- Reads API/model/agent options from the sidebar.
- Accepts an uploaded screenshot.
- Resizes the image for model-friendly processing.
- Builds a list of enabled agents.
- Creates a LangGraph workflow with `build_graph(enabled_agents)`.
- Stores the generated `DesignReport` in `st.session_state`.

The session-state storage is important because Streamlit reruns the script after interactions like clicking `Details`, opening expanders, or toggling checkboxes. Persisting the report keeps the analysis visible without rerunning the expensive LLM flow.

### 2. Graph Orchestration

[agents/graph.py](agents/graph.py) builds a LangGraph state machine:

```text
START
  -> retrieve
      -> visual  -> synthesize
      -> ux      -> synthesize
      -> market  -> synthesize
      -> live_research -> synthesize
  -> END
```

Only selected agents are added to the graph. The retrieval node always runs first so every enabled agent receives the same design context. Live Research is independent from Market Research and can run even when Market Research is disabled.

The graph state includes:

- `image_base64`
- `api_key`
- `model`
- `tavily_api_key`
- `retrieval_context`
- `visual_result`
- `ux_result`
- `market_result`
- `live_research_result`
- `synthesis`

### 3. Retrieval

[retrieval/retriever.py](retrieval/retriever.py) queries the local LanceDB database using a CLIP image embedding:

- `design_text` returns relevant design guidelines.
- `design_images` returns visually similar reference images when available.

If the knowledge base is not ready, the graph returns an empty `RetrievalContext` and the agents still run.

### 4. Specialist Agents

The app has four analysis agents:

- [agents/visual_analysis.py](agents/visual_analysis.py): color, typography, layout, spacing, visual hierarchy.
- [agents/ux_critique.py](agents/ux_critique.py): Nielsen heuristics, accessibility, interaction patterns.
- [agents/market_research.py](agents/market_research.py): product category, trend alignment, competitor positioning, differentiation.
- [agents/live_research.py](agents/live_research.py): Tavily web search for current trends, competitor benchmarks, opportunities, and source links.

The LLM-based agents:

- Calls OpenRouter through `ChatOpenAI`.
- Sends the uploaded screenshot as a base64 image.
- Includes retrieved design guidelines as context.
- Requests JSON output.
- Parses the response into a Pydantic result model.
- Falls back to a structured error result if the API call or JSON parsing fails.

The Live Research agent uses the official `langchain-tavily` integration. It first asks the configured LLM to create three search queries from the screenshot, runs fast Tavily searches, dedupes source URLs, and asks the LLM to summarize the retrieved snippets. If no `TAVILY_API_KEY` is provided, it returns a skipped result instead of blocking the full analysis.

### 5. Synthesis

[agents/synthesizer.py](agents/synthesizer.py) combines whichever specialist outputs are available into one executive report:

- Executive summary
- Overall score
- Top strengths
- Top recommendations
- Priority actions

Live Research has no numeric score. Its findings can influence recommendations, but skipped or unscored live research does not drag the overall score up or down.

### 6. Rendering

[ui/report_renderer.py](ui/report_renderer.py) renders:

- Overall synthesis card
- Priority action checklist
- Specialist score cards
- Live Research card with source count
- Detail dialogs for each selected agent
- Source links and snippets for live research

[ui/components.py](ui/components.py) contains smaller reusable UI helpers, including score badges and reference image rendering.

## Data Models

[models/schemas.py](models/schemas.py) defines the app contracts:

- `RetrievalContext`
- `RetrievedTextChunk`
- `RetrievedImage`
- `VisualAnalysisResult`
- `UXCritiqueResult`
- `MarketResearchResult`
- `WebResearchSource`
- `LiveResearchResult`
- `SynthesisResult`
- `DesignReport`
- `GraphState`

These schemas are the glue between retrieval, agents, graph state, and UI rendering.

## Knowledge Base

The knowledge base sources live in [knowledge_base/sources](knowledge_base/sources). The current sources include design principles, Apple HIG, Material Design, WCAG/accessibility, Nielsen heuristics, UX laws, component patterns, and design trends.

To rebuild the LanceDB index:

```bash
python knowledge_base/ingest.py
```

The ingestion pipeline:

1. Parses markdown files into sections and chunks.
2. Extracts text and images from PDFs if present.
3. Loads optional reference images from `knowledge_base/sources/reference_images/`.
4. Embeds text and images with CLIP.
5. Stores vectors in LanceDB under `knowledge_base/lancedb_data`.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file or enter keys in the sidebar:

```bash
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=optional_tavily_key
LANGSMITH_API_KEY=optional_langsmith_key
```

`OPENROUTER_API_KEY` is required to run analysis. `TAVILY_API_KEY` is optional; when it is missing, Live Research is skipped with a visible notice and the rest of the analysis continues.

Run the app:

```bash
streamlit run app.py
```

If the default port is busy, choose another:

```bash
streamlit run app.py --server.port 8560
```

## Configuration

[config/settings.py](config/settings.py) contains:

- LanceDB and source paths
- CLIP model settings
- Available OpenRouter model IDs
- Retrieval limits
- Max image size
- Text chunking settings

To add a new model, add its OpenRouter model ID to `AVAILABLE_MODELS`.

## Adding A New Agent

To add another specialist analysis agent:

1. Create a new agent module in `agents/`.
2. Add a Pydantic result schema in `models/schemas.py`.
3. Add the new field to `GraphState`, `AgentState`, and `DesignReport`.
4. Add a graph node in `agents/graph.py`.
5. Add a sidebar checkbox and enabled-agent key in `app.py`.
6. Add rendering support in `ui/report_renderer.py`.

Follow the existing agent pattern: accept `image_base64`, `retrieval_context`, `api_key`, and `model`, then return a structured Pydantic result. Agents that call external services should return a skipped or structured error result instead of stopping the full graph when optional credentials are missing.

## Verification

Useful checks:

```bash
python -m py_compile app.py ui/report_renderer.py agents/graph.py agents/live_research.py agents/synthesizer.py models/schemas.py
python -c "from agents.graph import build_graph; [build_graph(a) for a in [['visual', 'ux', 'market'], ['live_research'], ['visual', 'ux', 'market', 'live_research']]]; print('graph ok')"
```

For a full manual test:

1. Start Streamlit.
2. Upload a screenshot.
3. Enter an OpenRouter API key.
4. Run analysis without a Tavily key and confirm Live Research shows a skipped notice.
5. Add a Tavily key, rerun analysis, and confirm the Live Research card includes source count and source links.
6. Open each `Details` dialog.
7. Toggle priority actions and confirm the report remains visible.

## Deployment (Hugging Face Spaces, $0)

The whole app — UI, LangGraph agents, and the in-process CLIP embedding — runs as a single
Streamlit process. It deploys as one Hugging Face Space. Persistent shared history lives in a
free Qdrant Cloud cluster; the read-only reference knowledge base (`lancedb_data` + reference
images) ships committed in the repo, so the Space needs no scrape/ingest at runtime.

### Storage backends

History uses Qdrant when `QDRANT_URL` is set, and a local on-disk LanceDB store otherwise (see
[knowledge_base/history_store.py](knowledge_base/history_store.py), `get_history_store()`). So:

- **On the Space:** set `QDRANT_URL` → persistent, shared history (the Space disk is ephemeral).
- **Locally:** set the same `QDRANT_URL` to share one history with the Space, or leave it unset to
keep a separate on-disk history under `history/`.

### One-time setup

1. **Qdrant Cloud** — create a free 1GB cluster at `cloud.qdrant.io`; copy the cluster URL + an API key.
2. **Hugging Face** — create a new **Space** → SDK **Docker** → **CPU basic (free)** hardware. The
  committed `Dockerfile` installs deps (CPU torch) and runs `streamlit run app.py` on port 8501.
   Make it **private** so your `OPENROUTER_API_KEY` is not spent by random visitors.
3. **Space → Settings → Secrets** — add `OPENROUTER_API_KEY`, `TAVILY_API_KEY`, `QDRANT_URL`,
  `QDRANT_API_KEY` (and optional `LANGSMITH_API_KEY`). The sidebar prefills from these.
4. **Push the repo** to the Space's git remote:
  ```bash
   git init && git add -A && git commit -m "Deploy design analysis suite"
   git remote add space https://huggingface.co/spaces/<user>/<space-name>
   git push space main      # authenticate with `huggingface-cli login` if prompted
  ```

First boot installs dependencies and downloads the CLIP weights (cold start ~1–2 min). The
`design_history` collection is created automatically on the first analysis. The free Space sleeps
when idle and wakes on the next visit.
