import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http import models
from src.vector_store.qdrant_db import get_qdrant_client, embedding_model

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROGRESS_FILE = "data/crawled/progress.json"

def load_progress():
    """Loads the progress tracking file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_progress(progress):
    """Saves the progress tracking file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def ingest_documents(directory_path: str, collection_name: str):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    client = get_qdrant_client()
    progress = load_progress()
    
    # Check if the collection already exists and recreate it if necessary
    collections = client.get_collections().collections
    if not any(collection.name == collection_name for collection in collections):
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
        )

    # Load documents from the specified directory
    documents_to_ingest = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            if progress.get(file_path, {}).get("ingested"):
                print(f"Skipping already ingested file: {filename}")
                continue
            
            loader = TextLoader(file_path)
            documents_to_ingest.extend(loader.load())
            progress[file_path] = {"ingested": True}

    if not documents_to_ingest:
        print(f"No new documents to ingest in {directory_path}.")
        return

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents_to_ingest)

    # Add documents to Qdrant
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding_model,
    )
    vector_store.add_documents(chunks)
    save_progress(progress)
    print(f"Successfully ingested {len(chunks)} chunks into Qdrant collection '{collection_name}'.")
