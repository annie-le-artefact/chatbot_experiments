# Implementation Plan: Intelligent Dialog System

## 1. Executive Summary
This document outlines the roadmap for building an Enhanced Dialog Flow architecture. The approach prioritizes a **Proof of Concept (POC)** first strategy, validating the **Multi-Agent RAG** logic in a terminal environment before introducing UI layers, cloud infrastructure, or complex knowledge graphs.

## 2. Technology Stack

### Application Layer
* **Orchestration:** **LangGraph** (Stateful multi-agent workflows).
* **Language Model:** **LLM of choice** (e.g., GPT-4o, Claude 3.5 Sonnet, or Vertex AI).
* **Interface (Phase 3+):** **Chainlit** (Chat interface).
* **Authentication (Phase 3+):** **Google OAuth 2.0**.

### Data Layer
* **Vector Store:** **Weaviate** (Cloud-native, supports hybrid search).
* **Knowledge Graph (Phase 5):** **Neo4j** (For regulatory/structured data).

### Infrastructure & DevOps
* **Containerization:** Docker.
* **Orchestration:** **Kubernetes (GKE)** via **Helm Charts**.
* **CI/CD:** **Google Cloud Build**.
* **Observability:** **Prometheus** & Grafana.

---

## 3. Implementation Phases

### Phase 1: The Core Logic POC (Terminal-Based)
**Objective:** Validate the "Intelligent Routing" and "Data Retrieval" logic without UI or Cloud overhead.
* **Focus:** Pure Python logic + Local Vector Store.
* **Diagram Mapping:** *Intelligent Routing, Single-shot query, Multi-agent query, Data Retrieval (Vector Store only).*
* **Tasks:**
    * **Environment:** Set up local Docker for Weaviate.
    * **Ingestion:** Write scripts to chunk and vectorise distinct datasets (e.g., "Handbooks").
    * **LangGraph Agent:** Implement the router:
        * *Router Node:* Classify input -> Simple vs. Complex.
        * *RAG Node:* Query Weaviate -> Generate Answer.
    * **Interaction:** Build a simple `while True:` Python terminal loop for testing.
* **Deliverable:** A CLI tool where a user inputs a question and receives a cited answer.

### Phase 2: Infrastructure Foundation
**Objective:** Transition from "Localhost" to "Cloud-Ready" architecture.
* **Focus:** Containerization and Deployment pipelines.
* **Diagram Mapping:** *Orchestration (Infrastructure).*
* **Tasks:**
    * **Dockerize:** Create `Dockerfile` for the Python application.
    * **Helm Charts:**
        * Configure `charts/weaviate` for the vector store.
        * Configure `charts/app` for the agent application.
    * **CI/CD:** Configure **Google Cloud Build** triggers to build images on git push.
    * **Observability:** Deploy **Prometheus** sidecars to scrape basic application metrics (latency, error rates).
* **Deliverable:** The Phase 1 logic running inside a Kubernetes cluster.

### Phase 3: The User Interface Layer
**Objective:** Enable human-friendly interaction and security.
* **Focus:** UI integration and Auth.
* **Diagram Mapping:** *User Interface Layer, Orchestration (Auth, Rate Limiting).*
* **Tasks:**
    * **UI Swap:** Replace the Python terminal loop with **Chainlit** event handlers (`@cl.on_message`).
    * **Authentication:** Implement **Google OAuth** middleware.
    * **Session State:** Manage conversation history within the Chainlit user session.
    * **Rate Limiting:** Add basic middleware to prevent abuse.
* **Deliverable:** A secure web link where users can log in and chat.

### Phase 4: Trust, Safety & Guardrails
**Objective:** Ensure compliance and reliability.
* **Focus:** Output quality and safety checks.
* **Diagram Mapping:** *Final Safety Guardrails, Reasoning & Validation.*
* **Tasks:**
    * **Evaluation:** Establish a "Golden Dataset" and run automated evals (using LangSmith or similar) to measure retrieval accuracy.
    * **Guardrails Node:** Add a final node in LangGraph to scan for PII, toxicity, or hallucinations before showing the user the answer.
    * **Citations:** Enforce strict citation formatting in the output.
* **Deliverable:** A robust system that refuses to answer unsafe questions and cites sources accurately.

### Phase 5: Advanced Data Retrieval (Knowledge Graph)
**Objective:** Handle complex regulatory logic.
* **Focus:** Hybrid Retrieval (Vector + Graph).
* **Diagram Mapping:** *Data Retrieval (Knowledge Graph), Context Enrichment.*
* **Tasks:**
    * **Infrastructure:** Add **Neo4j** to the Helm charts.
    * **Ingestion:** Map regulatory documents into graph relationships (e.g., `Regulation -> Requires -> Action`).
    * **Logic Update:** Update the LangGraph *Router* to direct regulatory questions to the Graph Tool and general questions to the Vector Tool.
* **Deliverable:** The "Enhanced Dialog Flow" fully realized with hybrid intelligence.

