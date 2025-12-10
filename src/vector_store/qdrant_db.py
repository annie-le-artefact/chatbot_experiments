import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Initialize the embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=os.environ["GEMINI_API_KEY"])

def get_qdrant_client():
    """Initializes and returns a Qdrant client."""
    return QdrantClient(host="localhost", port=6333)

def get_retriever(client, collection_name="web_content"):
    """Creates and returns a Qdrant retriever."""
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding_model,
    )
    return vector_store.as_retriever()
