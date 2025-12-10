# Gemini Project Context: Intelligent Dialog System

## Project Overview

This project is a Proof of Concept (POC) for a terminal-based intelligent dialog system. It implements a Retrieval Augmented Generation (RAG) architecture to answer questions based on a local knowledge base.

The system is built in Python and leverages several key technologies:
- **Orchestration:** LangGraph is used to define the flow of logic, starting with a simple router that directs queries to a RAG chain.
- **Language Model:** The system uses a Google Gemini model for language understanding and generation.
- **Vector Store:** Qdrant serves as the vector database, running in a local Docker container.
- **Data Ingestion:** Scripts are provided to process and vectorize documents.

## Building and Running

### Prerequisites
- Docker
- Python 3.9+ & Conda

### 1. Set Up Environment

**a. Start Qdrant:**
```bash
docker-compose up -d
```

**b. Configure API Key:**
Create a `.env` file in the project root and add your Gemini API key.
```
GEMINI_API_KEY="your_gemini_api_key_here"
```

**c. Install Dependencies:**
```bash
conda env create -f environment.yml
```
This creates the `chatbot_experiments` environment and installs dependencies from `requirements.txt`.

### 2. Run the Application
To ensure commands are run in the correct environment, prepend them with `conda run -n chatbot_experiments`.
```bash
conda run -n chatbot_experiments python src/main.py --crawl
```

To stop the application, type `exit` in the terminal.

## Development Workflow

This project follows a strict, plan-driven development process. All work must adhere to the following workflow.

### The Phase-Based Development Cycle

Development is organized into **phases** (for new features) and **fixes** (for bug fixes), each defined in a `.json` file. The entire phase or fix should be treated as a single, atomic unit of work.

1.  **Plan:**
    *   Before any work begins, a comprehensive plan must be documented in a `phases/phase-xxx.json` or `fixes/fix-xxx.json` file.
    *   The plan will contain a list of smaller tasks or steps.
    *   This plan must be approved by the user.

2.  **Implement & Verify (per task):**
    *   Work through each task in the plan file sequentially.
    *   For each task:
        *   Update its `status` to `in_progress` in the `.json` file.
        *   Implement the necessary code.
        *   Test and verify that the changes work as expected and do not introduce regressions.
        *   For example: `conda run -n chatbot_experiments python src/main.py --crawl`
        *   If bugs are found, they should be addressed before moving on.
        *   Once the task is complete, update its `status` to `completed`.

3.  **Commit (per phase/fix):**
    *   **Only after all tasks** in the phase or fix are `completed` can the changes be committed.
    *   Create a single new branch for the entire phase or fix (e.g., `feature/phase-2` or `fix/db-connection`).
    *   Stage all relevant files (`git add .`).
    *   Commit the changes with a single, comprehensive message that summarizes the objective of the phase or fix. This message should be defined in the plan file.

4.  **Update Plan on Completion:**
    *   After the commit is successful, update the overall `status` of the phase or fix to `completed`.
    *   Record the final timestamp and the full `commit_hash` at the top level of the plan file.