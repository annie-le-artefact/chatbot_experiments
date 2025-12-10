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

This project validates RAG logic in a terminal environment. It uses LangGraph for orchestration, a Gemini LLM for generation, and Weaviate for vector storage. The system ingests data from external web pages via a sophisticated, resumable pipeline.

## 2. Features

*   **Local Weaviate:** Runs a local Docker instance of Weaviate for vector storage.
*   **Intelligent Web Ingestion Pipeline:** A fully automated, resumable pipeline that:
    1.  **Crawls:** Uses Playwright to fetch JavaScript-rendered HTML from URLs in `data/data_sources.json`.
    2.  **Processes:** Extracts clean text from the HTML, preserving structure.
    3.  **Translates:** Performs document-level translation to English using a Gemini LLM.
    4.  **Chunks & Ingests:** Splits the translated text into semantically coherent chunks and stores them in Weaviate with metadata.
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
    GEMINI_API_KEY="your_gemini_api_key_here"
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

To ensure commands are run in the correct environment, prepend them with `conda run -n chatbot_experiments`.

### 4.1 Ingesting Web Content
To run the entire resumable pipeline (crawl, process, translate, and ingest into Weaviate), use the `--crawl` flag:
```bash
conda run -n chatbot_experiments python src/main.py --crawl
```
This single command will manage all steps. If interrupted, you can run it again to resume where it left off.

### 4.1.1 Testing the Ingestion Process
To test the chunking and ingestion directly, run the `ingest.py` script:
```bash
conda run -n chatbot_experiments python src/ingestion/ingest.py
```
**Prerequisites:**
*   Weaviate must be running (`docker-compose up -d`).
*   Your Conda environment (`chatbot_experiments`) must be created.
*   A valid `GEMINI_API_KEY` must be set in your `.env` file.
*   At least one translated English text file (`_en.txt`) must exist in `data/crawled/processed/`.

**What to Expect:**
The script will ingest new or updated `_en.txt` files, chunk them, and load them into the `WebContent` collection in Weaviate. Afterwards, it will display the first 5 ingested chunks, including their source URL, title, chunk index, and content snippet.

### 4.2 Running the Chatbot
Once data has been ingested, you can start the dialog system for Q&A:
```bash
conda run -n chatbot_experiments python src/main.py
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
├── environment.yml
├── GEMINI.md
├── phases/
├── PROGRESS_LOG.md
└── README.md
```