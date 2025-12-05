# Gemini Project Context: Intelligent Dialog System

## Project Overview

This project is a Proof of Concept (POC) for a terminal-based intelligent dialog system. It implements a Retrieval Augmented Generation (RAG) architecture to answer questions based on a local knowledge base.

The system is built in Python and leverages several key technologies:
- **Orchestration:** LangGraph is used to define the flow of logic, starting with a simple router that directs queries to a RAG chain.
- **Language Model:** The system uses a Google Gemini model (e.g., `gemini-pro`) for language understanding and generation, accessed via the `langchain-google-genai` library.
- **Vector Store:** Weaviate serves as the vector database, running in a local Docker container. It stores vectorized chunks of documents for efficient similarity search.
- **Data Ingestion:** A script (`src/ingestion/ingest.py`) is provided to process text files from a `data/handbooks` directory, chunk them, generate embeddings using the Gemini model, and store them in Weaviate.

The project follows a multi-phase implementation plan (`plan.md`), with the current focus being **Phase 1: The Core Logic POC**. The goal is to validate the RAG pipeline in a simple, terminal-based environment before adding a UI or cloud infrastructure.

## Building and Running

### Prerequisites
- Docker
- Python 3.9+ and `pip`

### 1. Set Up Environment

**a. Start Weaviate:**
The vector database runs in a Docker container.
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
pip install -r requirements.txt
```

### 2. Run the Application

There are two modes for running the application, controlled by the `--ingest` flag.

**a. Ingest Data and Start Chat:**
This command will first delete any existing "Handbooks" collection in Weaviate, then process the text files in `data/handbooks`, and finally start the interactive chat loop.
```bash
python src.py --ingest
```

**b. Start Chat Only:**
If the data has already been ingested, you can start the chat directly.
```bash
python src/main.py
```

To stop the application, type `exit` in the terminal.

## Development Workflow

This project follows a structured, plan-driven development process. All development work, whether for a multi-step project phase or a single bug fix, must adhere to this workflow.

### Plan-Driven Execution

All tasks are managed through `.json` plan files. The structure of these plans and the execution workflow are the same for all types of tasks.

-   **Phases:** For each major implementation phase outlined in `plan.md`, a corresponding `phase-xxx.json` file must be created in the `phases/` directory (e.g., `phases/phase_1.json`).
-   **Bug Fixes:** For bug fixes, a corresponding `fix-xxx.json` file must be created in the `fixes/` directory, where `xxx` is the issue identifier (e.g., `fixes/fix-123.json`).

### Operating Modes

There are two modes for development:

1.  **Plan Mode:** In this mode, a detailed, step-by-step plan is created to address a specific issue or feature. The plan is stored in the corresponding `.json` file and must be approved before execution begins.
2.  **Execute Mode:** Once a plan has been approved, it is executed step-by-step, with each step being committed to version control separately.

### Workflow Details

#### Phase 1: Prepare your git branch

- If git has been initialized, the git repo is in the root workspace folder.
- Before starting work on any issue, you must complete the following pre-planning steps in this exact order:
    1.  **Create and switch to branch:** Create a new branch named `feature/phase-[number]` for phases or `fix/issue-[id]` for bug fixes.
    2.  **Create the plan file:** Create the appropriate `phase-xxx.json` or `fix-xxx.json` file if it does not already exist.

#### Phase 2: Create a step-by-step plan

Create a numbered step-by-step plan to perform the work in the `.json` plan file. When creating the plan:

1.  **Practice Test-Driven Development (TDD):** Adhere to a TDD workflow. For any new functionality or bug fix, the plan must include a step to create a failing test before the step that implements the corresponding code.
2.  **Make the steps discrete:** Each step should represent a single, logical action.
3.  **Optimize for clarity and detail:** The prompts for each step must be descriptive, detailed, and unambiguous.
4.  **ALWAYS finish by creating a pull request.** The final step of every plan MUST be to create a pull request.

Each step within the plan file MUST be an object containing the following keys:

- **step:** (Integer) An incremental step number starting at 1.
- **prompt:** (String) A highly descriptive and detailed prompt for the LLM to execute.
- **status:** (String) The current status of the step. The initial state should be "pending".
- **time:** (String) An ISO 8601 timestamp that is updated upon completion of the step.
- **git:** (Object) An object containing git-related information:
    - **commit_message:** (String) The commit message for the step, following the format: `[Step X] <description>`.
    - **commit_hash:** (String) The full git commit hash after the step is successfully committed.

#### Phase 3: Request User Approval

**CRITICAL:** BEFORE executing any of the steps in the plan, you MUST present the plan to the user and ask for approval to continue.

#### Phase 4: Step-by-Step Execution

**AFTER** the user has approved the plan, you must execute the plan sequentially.

1.  Announce the step you are about to execute.
2.  If a step is unsuccessful, attempt to resolve the error. If you cannot, STOP and ask for help.
3.  After successfully completing a single step:
    - Stage and commit the changes with the precise message for that step.
    - Retrieve the commit hash.
    - Update the corresponding step in the plan file with the status, timestamp, and commit hash.
4.  Only proceed to the next step after all prior steps have been completed successfully.
