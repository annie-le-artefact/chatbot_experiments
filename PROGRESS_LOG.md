# Project Progress Log

This document tracks the setup, planning, and development progress of the Intelligent Dialog System project.

## I. Initial Project Setup & Planning

1.  **File Integration & Workflow:** Unified `software_developer.md` into `GEMINI.md` to establish a strict, plan-driven development workflow. Created `phases/` and `fixes/` directories to house `.json` plan files.
2.  **Phase 1 Completion:** Successfully implemented the core logic POC, including data ingestion from local text files and a terminal-based RAG chat interface. Marked `phases/phase_1.json` as complete.
3.  **Git Initialization:** Initialized a Git repository and configured `.gitignore` to exclude sensitive files, local data, and IDE settings.
4.  **Dependency Management:** Refactored `environment.yml` to be the single source of truth for Conda environment setup, pointing to `requirements.txt` for pip packages.

## II. Phase 2: Intelligent Ingestion Pipeline

To handle external web-based knowledge sources, a sophisticated, three-stage ingestion pipeline was designed and implemented.

1.  **Stage 1: Metadata-Aware Crawling (`crawler.py`):**
    *   **Problem:** Initial attempts to crawl websites failed because they required JavaScript to render content.
    *   **Solution:** The crawler was re-implemented using **Playwright** (a headless browser) to ensure full page rendering.
    *   **Features:**
        *   Reads URLs from `data/data_sources.json`.
        *   Infers metadata (jurisdiction, year, doc_type) from the source.
        *   Saves the fully-rendered HTML in a structured JSON format (`DK-LAW-2023-835.json`) to `data/crawled/structured/`.
        *   **Resumable:** Tracks progress in `data/crawled/progress.json` to avoid re-crawling completed URLs.

2.  **Stage 2: Processing (`processor.py`):**
    *   **Features:**
        *   Reads the structured JSON files produced by the crawler.
        *   Uses `BeautifulSoup` to parse the HTML and extract clean text.
        *   **Preserves line breaks** to maintain document structure.
        *   Saves the clean, original-language text to `_dk.txt` files in `data/crawled/processed/`.
        *   **Resumable:** Uses `progress.json` to skip already-processed files.

3.  **Stage 3: Translation (`translator.py`):**
    *   **Problem:** Translation was initially attempted on a per-chunk basis, which was inefficient. A `ModuleNotFoundError` also blocked progress due to dependency conflicts.
    *   **Solution:**
        *   The dependency conflict was resolved by upgrading `langchain` and `langchain-google-genai` to their latest compatible versions.
        *   The script was re-designed to perform **document-level translation** for much greater efficiency.
    *   **Features:**
        *   Reads the clean `_dk.txt` files.
        *   Uses the `gemini-pro-latest` LLM to translate the entire document's text to English.
        *   Saves the translated text to `_en.txt` files in `data/crawled/processed/`.
        *   **Resumable:** Uses `progress.json` to skip already-translated files.

## III. Bug Fixes

The following critical bugs were resolved during development:

*   **Missing `text_key` Argument:** Fixed `TypeError` in `WeaviateVectorStore` initialization.
*   **`None` Embedding:** Ensured user queries are vectorized before similarity search.
*   **`gemini-pro` Model Not Found:** Updated to a stable, versioned model name (`gemini-1.0-pro` and later `gemini-pro-latest`).
*   **Weaviate Connection `ResourceWarning`:** Refactored client handling to ensure connections are properly closed.
*   **JavaScript Rendering Failure:** Replaced `requests` with `Playwright` in the crawler.
*   **`langchain_core` `ModuleNotFoundError`:** Resolved dependency conflicts by upgrading `langchain` packages.

## IV. Project Organization

*   Moved Gemini model-related files (`GEMINI_MODELS.md`, `list_gemini_models.py`) to a dedicated `src/gemini/` directory.