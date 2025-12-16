# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval Augmented Generation) system that ingests Danish legal and guidance documents, translates them to English, and provides a terminal-based Q&A interface. The system uses:
- **LangGraph** for orchestration
- **Gemini LLM** for generation and translation
- **Qdrant** (local Docker) for vector storage
- **Playwright** for web crawling with JavaScript rendering

## Common Commands

### Environment Setup
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Start Qdrant (required for all operations)
docker-compose up -d

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Install Playwright browsers (one-time setup)
playwright install
```

### Running the Application
Make sure your virtual environment is activated first:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Then run commands:
```bash
# Run the full ingestion pipeline (crawl → process → translate → ingest)
python -m src.main --crawl --dir data/crawled/processed

# Run the chatbot (after ingestion)
python -m src.main

# Use a different collection name
python -m src.main --crawl --collection my_collection
```

### Running Individual Pipeline Stages (for debugging)
```bash
# 1. Crawl: Fetch JavaScript-rendered HTML from URLs in data/data_sources.json
python -m src.ingestion.crawler

# 2. Process: Extract clean text from HTML
python -m src.ingestion.processor

# 3. Translate: Translate Danish text to English using Gemini
python -m src.ingestion.translator

# 4. Ingest: Chunk and store translated text in Qdrant
python -m src.ingestion.ingest
```

### Docker Management
```bash
# Stop Qdrant
docker-compose down

# View Qdrant logs
docker-compose logs -f qdrant

# Access Qdrant web UI
# http://localhost:6333/dashboard
```

## Architecture

### Ingestion Pipeline
The system uses a **resumable pipeline** tracked by `data/crawled/progress.json`. Each URL progresses through four stages:

1. **Crawl** (`src/ingestion/crawler.py`):
   - Fetches fully rendered HTML using Playwright (handles JavaScript)
   - Saves raw HTML + metadata to `data/crawled/structured/`
   - Generates filenames like `DK-LEGAL_DOCUMENTS-2023-835.json`
   - Marks URL as `crawled: true` in progress.json

2. **Process** (`src/ingestion/processor.py`):
   - Extracts clean text from HTML using BeautifulSoup
   - Removes nav, header, footer, scripts, styles
   - Saves Danish text to `data/crawled/processed/*_dk.txt`
   - Marks URL as `processed: true` in progress.json

3. **Translate** (`src/ingestion/translator.py`):
   - Translates entire document (not chunks) using Gemini LLM
   - Uses `gemini-pro-latest` model with temperature=0.0
   - Saves English text to `data/crawled/processed/*_en.txt`
   - Marks URL as `translated: true` in progress.json

4. **Ingest** (`src/ingestion/ingest.py`):
   - Loads all `*_en.txt` files from processed directory
   - Chunks text using RecursiveCharacterTextSplitter (chunk_size=1000, overlap=200)
   - Embeds chunks using `models/text-embedding-004`
   - Stores in Qdrant collection with 768-dimensional vectors (COSINE distance)
   - Marks file as `ingested: true` in progress.json

**Progress Tracking**: Each stage checks `progress.json` before processing. If interrupted, re-run the command to resume from where it stopped. To re-process a URL, manually edit `progress.json` to set the relevant flag to `false`.

### RAG Agent
The agent (`src/agent/router.py`) implements a simple RAG pattern:
- **Retriever**: Fetches relevant document chunks from Qdrant
- **LLM**: `gemini-2.0-flash` generates answers from retrieved context
- **Routing**: Currently always uses RAG (placeholder for future multi-agent logic)

### Vector Store
`src/vector_store/qdrant_db.py` provides:
- `get_qdrant_client()`: Connects to local Qdrant (localhost:6333)
- `embedding_model`: GoogleGenerativeAIEmbeddings with `models/text-embedding-004`
- `get_retriever()`: Returns LangChain Qdrant retriever for a collection

### Data Flow
```
data/data_sources.json (URLs)
    ↓ crawler.py (Playwright)
data/crawled/structured/*.json (raw HTML + metadata)
    ↓ processor.py (BeautifulSoup)
data/crawled/processed/*_dk.txt (clean Danish text)
    ↓ translator.py (Gemini LLM)
data/crawled/processed/*_en.txt (English text)
    ↓ ingest.py (LangChain + embeddings)
Qdrant collection (vector chunks)
    ↓ router.py (RAG)
User query → Answer
```

## Configuration

### Required Environment Variables
Create a `.env` file in the project root:
```
GEMINI_API_KEY="your_gemini_api_key_here"
```

### Data Sources
Edit `data/data_sources.json` to add/remove URLs for ingestion. Structure:
```json
{
  "domain.com": {
    "base_url": "https://domain.com",
    "type": "legal_documents",
    "pages": [
      {"url": "https://domain.com/page", "title": "Page Title"}
    ]
  }
}
```

### Qdrant Configuration
- Port: 6333 (API), 6334 (gRPC)
- Data persisted in `./qdrant_data/`
- Default collection: `web_content`

## Key Files

- `src/main.py`: Entry point with CLI argument parsing
- `src/agent/router.py`: RAG chain creation and query processing
- `src/vector_store/qdrant_db.py`: Qdrant client and embedding initialization
- `src/ingestion/`: Pipeline modules (crawler, processor, translator, ingest)
- `data/crawled/progress.json`: Pipeline state tracking (resumable)
- `data/data_sources.json`: URLs to ingest
- `requirements.txt`: Python dependencies
- `docker-compose.yml`: Qdrant service definition

## Development Notes

### Working with the Pipeline
- The pipeline is designed to be **idempotent and resumable**. Re-running any stage skips already-processed items.
- To force re-processing of a specific URL, edit `data/crawled/progress.json` and set the relevant flag (`crawled`, `processed`, `translated`, `ingested`) to `false`.
- The ingestion process tracks files (not URLs), so `progress.json` uses file paths as keys for the `ingested` flag.

### LLM Models Used
- **Translation**: `gemini-pro-latest` (temperature=0.0 for consistency)
- **Embeddings**: `models/text-embedding-004` (768 dimensions)
- **RAG Generation**: `gemini-2.0-flash`

### Chunking Strategy
The system uses `RecursiveCharacterTextSplitter` with:
- `chunk_size=1000` characters
- `chunk_overlap=200` characters
This is applied to the translated English text, not the original Danish.

### Playwright Usage
The crawler uses Playwright in headless mode with Chromium. It waits 3 seconds after `domcontentloaded` to ensure JavaScript renders. To debug rendering issues, modify `crawler.py` to use `headless=False` in `launch()`.

### Collection Management
- Collection names default to `web_content` but can be customized via `--collection` flag
- Collections are created with `recreate_collection()` if they don't exist (deletes existing data)
- Vector dimension is hardcoded to 768 to match the embedding model

### Testing the RAG System
The `main.py` runs a single test query by default: "What is the risk of lower back pain?". Modify this query in `main.py:27` to test different scenarios.