import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.vector_store.qdrant_db import get_qdrant_client, get_retriever

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Initialize LLM with correct model name and API key parameter
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

def create_rag_chain(collection_name: str, client):
    retriever = get_retriever(client, collection_name=collection_name)

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
    
    client = get_qdrant_client()
    try:
        if route == "rag":
            rag_chain = create_rag_chain(collection_name, client)
            response = rag_chain.invoke(query)
        else:
            response = "I'm not sure how to handle this type of query yet."
        
        return response
    finally:
        pass

if __name__ == "__main__":
    # This part is for testing the agent logic directly
    # Ensure Qdrant is running and data is ingested using ingest.py
    pass
