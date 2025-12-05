import os
from dotenv import load_dotenv
import weaviate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

WEAVIATE_URL = "http://localhost:8080"
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY") # Not used if anonymous access is enabled
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_weaviate_client():
    client = weaviate.connect_to_local(
        host="localhost",
        port=8080,
    )
    return client

def ingest_documents(directory_path: str, collection_name: str):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    with get_weaviate_client() as client:
        if client.collections.exists(collection_name):
            print(f"Collection '{collection_name}' already exists. Deleting and recreating...")
            client.collections.delete(collection_name)

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

        # Initialize GoogleGenerativeAIEmbeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

        # Add documents to Weaviate
        vectorstore = WeaviateVectorStore.from_documents(
            client=client,
            documents=chunks,
            embedding=embeddings,
            by_text=False,
            collection_name=collection_name,
        )
        print(f"Successfully ingested {len(chunks)} chunks into Weaviate collection '{collection_name}'.")

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
        print("Please ensure Weaviate is running (docker-compose up -d) and your GEMINI_API_KEY is set.")
