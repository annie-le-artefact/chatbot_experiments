import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http import models
from src.vector_store.qdrant_db import get_qdrant_client, embedding_model

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ingest_documents(directory_path: str, collection_name: str):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    client = get_qdrant_client()
    
    # Check if the collection already exists and recreate it
    collections = client.get_collections().collections
    if any(collection.name == collection_name for collection in collections):
        print(f"Collection '{collection_name}' already exists. Deleting and recreating...")
        client.delete_collection(collection_name)

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )

    # Load documents from the specified directory
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            loader = TextLoader(file_path)
            documents.extend(loader.load())

    if not documents:
        print(f"No .txt documents found in {directory_path}. Exiting ingestion.")
        return

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    # Add documents to Qdrant
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding_model,
    )
    vector_store.add_documents(chunks)
    print(f"Successfully ingested {len(chunks)} chunks into Qdrant collection '{collection_name}'.")

if __name__ == "__main__":
    # Example usage: Ingest documents from data/handbooks into a collection named "Handbooks"
    # First, create some dummy handbook files in data/handbooks
    os.makedirs("data/handbooks", exist_ok=True)
    with open("data/handbooks/handbook_1.txt", "w") as f:
        f.write("This is the first handbook. It talks about company policies and procedures. Employee benefits are also detailed here.")
    with open("data/handbooks/handbook_2.txt", "w") as f:
        f.write("The second handbook focuses on IT guidelines and security protocols. Data privacy is a key concern.")

    try:
        ingest_documents("data/handbooks", "Handbooks")
    except Exception as e:
        print(f"An error occurred during ingestion: {e}")
        print("Please ensure Qdrant is running and your GEMINI_API_KEY is set.")
