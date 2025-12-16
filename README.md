# Intelligent Dialog System POC

This project is a Proof of Concept (POC) for a terminal-based intelligent dialog system that implements a Retrieval Augmented Generation (RAG) architecture.

## Table of Contents
1.  [Overview](#1-overview)
2.  [Features](#2-features)
3.  [Setup](#3-setup)
4.  [Usage](#4-usage)
    *   [4.1 Ingesting Web Content](#41-ingesting-web-content)
    *   [4.1.1 Testing the Ingestion Process](#411-testing-the-ingestion-process)
    *   [4.2 Running the Chatbot](#42-running-the-chatbot)
5.  [Project Structure](#5-project-structure)

## 1. Overview

This project validates RAG logic in a terminal environment. It uses LangGraph for orchestration, a Gemini LLM for generation, and Qdrant for vector storage. The system ingests data from external web pages via a sophisticated, resumable pipeline.

## 2. Features

*   **Local Qdrant:** Runs a local Docker instance of Qdrant for vector storage.
*   **Intelligent Web Ingestion Pipeline:** A fully automated, resumable pipeline that:
    1.  **Crawls:** Uses Playwright to fetch JavaScript-rendered HTML from URLs in `data/data_sources.json`.
    2.  **Processes:** Extracts clean text from the HTML, preserving structure.
    3.  **Translates:** Performs document-level translation to English using a Gemini LLM.
    4.  **Chunks & Ingests:** Splits the translated text into semantically coherent chunks and stores them in Qdrant with metadata.
*   **RAG Agent:** A LangGraph agent that performs RAG against the ingested data.
*   **Terminal Interaction:** A simple CLI for interactive Q&A.

## 3. Setup

### Prerequisites
*   Docker
*   Python 3.9+
*   [uv](https://docs.astral.sh/uv/) - Fast Python package installer

### Setup Steps
1.  **Install uv (if not already installed):**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **Start Qdrant:**
    ```bash
    docker-compose up -d
    ```
3.  **Configure API Key:**
    Create a `.env` file in the project root and add your Gemini API key:
    ```
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```
4.  **Create Virtual Environment and Install Dependencies:**
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    uv pip install -r requirements.txt
    ```
5.  **Install Playwright Browsers:**
    This one-time command is needed to download the browsers for the web crawler.
    ```bash
    playwright install
    ```

## 4. Usage

Make sure your virtual environment is activated before running commands:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4.1 Ingesting Web Content
To run the entire resumable pipeline (crawl, process, translate, and ingest into Qdrant), use the `--crawl` flag:
```bash
python -m src.main --crawl --dir data/crawled/processed
```
This single command will manage all steps. If interrupted, you can run it again to resume where it left off.

### 4.1.1 Testing the Ingestion Process
To test the chunking and ingestion directly, you can run the `ingest.py` script, although it's recommended to use the `main.py` script as shown above.

**Prerequisites:**
*   Qdrant must be running (`docker-compose up -d`).
*   Virtual environment must be activated.
*   A valid `GEMINI_API_KEY` must be set in your `.env` file.
*   At least one translated English text file (`_en.txt`) must exist in `data/crawled/processed/`.

**What to Expect:**
The script will ingest new or updated `_en.txt` files, chunk them, and load them into the `web_content` collection in Qdrant.

### 4.2 Running the Chatbot
Once data has been ingested, you can start the dialog system for Q&A:
```bash
python -m src.main
```

## 5. Project Structure
```
.
├── data/
│   ├── crawled/
│   │   ├── processed/
│   │   ├── structured/
│   │   └── progress.json
│   └── data_sources.json
├── src/
│   ├── agent/
│   ├── gemini/
│   └── ingestion/
├── .gitignore
├── docker-compose.yml
├── GEMINI.md
├── phases/
├── PROGRESS_LOG.md
└── README.md
```