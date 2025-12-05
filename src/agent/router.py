import os
from dotenv import load_dotenv
import weaviate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

WEAVIATE_URL = "http://localhost:8080"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Initialize LLM with correct model name and API key parameter
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)
embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

def get_weaviate_client():
    client = weaviate.connect_to_local(
        host="localhost",
        port=8080,
    )
    return client

def get_retriever(collection_name: str, embedder, client):
    collection = client.collections.get(collection_name)
    vectorstore = WeaviateVectorStore(client=client, index_name=collection_name, text_key="text", embedding=embedder)
    return vectorstore.as_retriever()

def create_rag_chain(collection_name: str, client):
    retriever = get_retriever(collection_name, embedder, client)

    template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question}
Context: {context}
Answer:"""
    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | prompt 
        | llm 
        | StrOutputParser()
    )
    return rag_chain

# This is a very simple router. In a real application, this would be more sophisticated.
def route_query(query: str) -> str:
    # For POC, always use the RAG chain for now.
    # In future phases, this would classify if it's a simple query vs. complex requiring multi-agent.
    return "rag"

def process_query(query: str, collection_name: str):
    route = route_query(query)
    
    with get_weaviate_client() as client:
        try:
            if route == "rag":
                rag_chain = create_rag_chain(collection_name, client)
                response = rag_chain.invoke(query)
            else:
                response = "I'm not sure how to handle this type of query yet."
            
            return response
        finally:
            pass # Client is closed by the with statement

if __name__ == "__main__":
    # This part is for testing the agent logic directly
    # Ensure Weaviate is running and data is ingested using ingest.py
    
    # For testing, we can use a dummy collection or ensure 'Handbooks' is ingested.
    # print("Attempting to process a query...")
    # test_query = "What are the company policies?"
    # try:
    #     response = process_query(test_query, "Handbooks")
    #     print(f"Query: {test_query}\nResponse: {response}")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     print("Please ensure Weaviate is running (docker-compose up -d) and data is ingested.")
    pass
