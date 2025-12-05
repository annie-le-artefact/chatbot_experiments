# Intelligent Dialog System POC

This project is a Proof of Concept (POC) for an Intelligent Dialog System, focusing on validating multi-agent RAG (Retrieval Augmented Generation) logic in a terminal environment.

## Table of Contents
1.  [Overview](#1-overview)
2.  [Phase 1: Core Logic POC](#2-phase-1-core-logic-poc)
    *   [Objective](#objective)
    *   [Features](#features)
3.  [Setup](#3-setup)
    *   [Prerequisites](#prerequisites)
    *   [Weaviate](#weaviate)
    *   [Environment Variables](#environment-variables)
    *   [Installation](#installation)
4.  [Usage](#4-usage)
    *   [Data Ingestion](#data-ingestion)
    *   [Running the Dialog System](#running-the-dialog-system)
5.  [Project Structure](#5-project-structure)
6.  [Next Steps](#6-next-steps)

## 1. Overview

The Intelligent Dialog System aims to build an enhanced dialog flow architecture. This POC focuses on the foundational elements of intelligent routing and data retrieval using LangGraph for orchestration and Weaviate as a vector store.

## 2. Phase 1: Core Logic POC

### Objective
Validate the "Intelligent Routing" (basic routing) and "Data Retrieval" (RAG with Weaviate) logic without UI or cloud infrastructure overhead. The current implementation is a terminal-based CLI tool.

### Features
*   **Local Weaviate:** Uses a local Docker instance of Weaviate for vector storage.
*   **Data Ingestion:** Scripts to chunk and vectorize text datasets (e.g., "Handbooks") into Weaviate.
*   **RAG Agent:** A basic LangGraph agent that performs RAG against the ingested data.
*   **Terminal Interaction:** A simple `while True:` loop for CLI-based interaction.

## 3. Setup

### Prerequisites
*   Docker (for Weaviate)
*   Python 3.9+
*   `pip` (Python package installer)

### Weaviate
Weaviate is used as the vector database. It is configured to run locally via Docker.

1.  **Start Weaviate:**
    Navigate to the project root and run:
    ```bash
    docker-compose up -d
    ```
    This will start the Weaviate container in the background, exposing ports `8080` (HTTP) and `50051` (gRPC).

### Environment Variables
Create a `.env` file in the project root and add your Google Gemini API key:

```
GEMINI_API_KEY="your_gemini_api_key_here"
```

**Note:** The `.env` file is ignored by Git (see `.gitignore`).

### Installation
1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd chatbot_experiments
    ```
2.  **Create and activate Conda environment:**
    ```bash
    conda env create -f environment.yml
    conda activate chatbot_experiments
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 4. Usage

### Data Ingestion
Before you can query the system, you need to ingest data into Weaviate. The `src/ingestion/ingest.py` script handles this. For this POC, dummy handbook files (`data/handbooks/handbook_1.txt`, `data/handbooks/handbook_2.txt`) are created and ingested.

To run ingestion and then start the chat loop:

```bash
python src/main.py --ingest
```

### Running the Dialog System
Once Weaviate is running and data has been ingested, you can start the dialog system:

```bash
python src/main.py
```

You can then type questions in the terminal, and the agent will respond using the ingested context.

Example interaction:

```
Welcome to the Intelligent Dialog System POC!
Type 'exit' to quit.
You: What are the company policies?
Agent: This is the first handbook. It talks about company policies and procedures. Employee benefits are also detailed here.
You: What about IT guidelines?
Agent: The second handbook focuses on IT guidelines and security protocols. Data privacy is a key concern.
You: exit
```

## 5. Project Structure

```
.gemini/
├── tmp/
flow diagram.png
plan.md
docker-compose.yml
.env
.gitignore
README.md
requirements.txt
src/
├── __init__.py
├── agent/
│   ├── __init__.py
│   └── router.py
├── ingestion/
│   ├── __init__.py
│   └── ingest.py
└── main.py
data/
└── handbooks/
    ├── handbook_1.txt (created during ingestion)
    └── handbook_2.txt (created during ingestion)
```

## 6. Next Steps
Refer to `plan.md` for subsequent phases, including infrastructure foundation (Phase 2), UI layer (Phase 3), trust & safety (Phase 4), and advanced data retrieval with knowledge graphs (Phase 5).
