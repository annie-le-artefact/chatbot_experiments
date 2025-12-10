import argparse
from dotenv import load_dotenv
from src.ingestion.ingest import ingest_documents
from src.agent.router import process_query

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Intelligent Dialog System POC")
    parser.add_argument("--crawl", action="store_true", help="Run the web content ingestion pipeline before starting the chat loop.")
    parser.add_argument("--dir", type=str, default="data/crawled/processed", help="Directory to crawl for documents.")
    parser.add_argument("--collection", type=str, default="web_content", help="Name of the collection to ingest documents into.")
    args = parser.parse_args()

    if args.crawl:
        print(f"Running web content ingestion pipeline from directory: {args.dir}")
        try:
            ingest_documents(args.dir, args.collection)
            print("Web content ingestion complete.")
        except Exception as e:
            print(f"Error during web content ingestion: {e}")
            print("Please ensure Qdrant is running and your GEMINI_API_KEY is set.")
        return

    print("\n--- Running a single test query ---")
    
    test_query = "What is the risk of lower back pain?"
    print(f"Query: {test_query}")

    try:
        response = process_query(test_query, args.collection)
        print(f"Agent: {response}")
    except Exception as e:
        print(f"Agent: An error occurred while processing your query: {e}")
        print("Please ensure Qdrant is running and data is ingested.")
    
    print("\n--- Test query complete ---")


if __name__ == "__main__":
    main()