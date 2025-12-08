# Intelligent Dialog System POC

This project is a Proof of Concept (POC) for a terminal-based intelligent dialog system that implements a Retrieval Augmented Generation (RAG) architecture.

## Table of Contents
1.  [Overview](#1-overview)
2.  [Features](#2-features)
3.  [Setup](#3-setup)
4.  [Usage](#4-usage)
    *   [4.1 Handbook Ingestion](#41-handbook-ingestion)
    *   [4.2 Web Content Ingestion Pipeline](#42-web-content-ingestion-pipeline)
    *   [4.3 Running the Chatbot](#43-running-the-chatbot)
5.  [Project Structure](#5-project-structure)

## 1. Overview

This project validates RAG logic in a terminal environment. It uses LangGraph for orchestration, a Gemini LLM for generation, and Weaviate for vector storage. The system can ingest data from local text files and external web pages.

## 2. Features

*   **Local Weaviate:** Runs a local Docker instance of Weaviate for vector storage.
*   **Handbook Ingestion:** Ingests local `.txt` files from the `data/handbooks/` directory.
*   **Intelligent Web Ingestion:** A robust, three-stage pipeline for ingesting web content:
    1.  **Crawl:** Uses a Playwright-based headless browser to fetch fully JavaScript-rendered HTML, saving it with inferred metadata.
    2.  **Process:** Extracts clean, structured text from the raw HTML, preserving line breaks.
    3.  **Translate:** Performs document-level translation from Danish to English using a Gemini LLM.
    *   **Resumable:** The entire web pipeline tracks progress and can be resumed at any time, avoiding redundant work.
*   **RAG Agent:** A LangGraph agent that performs RAG against the ingested data.
*   **Terminal Interaction:** A simple CLI for interactive Q&A.

## 3. Setup

### Prerequisites
*   Docker
*   Python 3.9+ & Conda

### Setup Steps
1.  **Start Weaviate:**
    ```bash
    docker-compose up -d
    ```
2.  **Configure API Key:**
    Create a `.env` file in the project root and add your Gemini API key:
    ```
    GEMINI_API_key="your_gemini_api_key_here"
    ```
3.  **Install Dependencies:**
    ```bash
    conda env create -f environment.yml
    conda activate chatbot_experiments
    ```
4.  **Install Playwright Browsers:**
    This one-time command is needed to download the browsers for the web crawler.
    ```bash
    playwright install
    ```

## 4. Usage

### 4.1 Handbook Ingestion
To ingest the local handbook text files and start the chat:
```bash
python src/main.py --ingest
```

### 4.2 Web Content Ingestion Pipeline
This is a three-step, resumable pipeline. Run these commands in order. If a step is interrupted, you can simply run it again to continue where it left off.

**Step 1: Crawl Raw HTML**
```bash
python src/ingestion/crawler.py
```
*Output: Raw, structured HTML JSON files in `data/crawled/structured/`.*

**Step 2: Process and Clean Text**
```bash
python src/ingestion/processor.py
```
*Output: Cleaned Danish text files (`*_dk.txt`) in `data/crawled/processed/`.*

**Step 3: Translate to English**
```bash
python src/ingestion/translator.py
```
*Output: Translated English text files (`*_en.txt`) in `data/crawled/processed/`.*

*(Note: The final ingestion of this translated content is handled in a later step of the project plan.)*

### 4.3 Running the Chatbot
Once data has been ingested, you can start the dialog system:
```bash
python src/main.py
```

## 5. Project Structure
```
.
├── data/
│   ├── crawled/
│   │   ├── processed/  (Cleaned & Translated Text)
│   │   ├── structured/ (Raw HTML as JSON)
│   │   └── progress.json
│   ├── data_sources.json
│   └── handbooks/
├── src/
│   ├── agent/
│   ├── gemini/         (Gemini model utilities)
│   └── ingestion/
│       ├── crawler.py
│       ├── processor.py
│       ├── translator.py
│       └── ingest.py
├── .gitignore
├── docker-compose.yml
├── environment.yml
├── GEMINI.md           (Project & Workflow Details)
├── phases/             (Development Plans)
├── plan.md
├── PROGRESS_LOG.md
└── README.md
```