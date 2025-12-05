import os
import argparse
from dotenv import load_dotenv
from ingestion.ingest import ingest_documents
from agent.router import process_query

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Intelligent Dialog System POC")
    parser.add_argument("--ingest", action="store_true", help="Run data ingestion before starting the chat loop.")
    args = parser.parse_args()

    collection_name = "Handbooks"
    handbooks_dir = "data/handbooks"

    if args.ingest:
        print("Running data ingestion...")
        # Create some dummy handbook files for ingestion example
        os.makedirs(handbooks_dir, exist_ok=True)
        with open(os.path.join(handbooks_dir, "handbook_1.txt"), "w") as f:
            f.write("This is the first handbook. It talks about company policies and procedures. Employee benefits are also detailed here.")
        with open(os.path.join(handbooks_dir, "handbook_2.txt"), "w") as f:
            f.write("The second handbook focuses on IT guidelines and security protocols. Data privacy is a key concern.")
        
        try:
            ingest_documents(handbooks_dir, collection_name)
            print("Ingestion complete.")
        except Exception as e:
            print(f"Error during ingestion: {e}")
            print("Please ensure Weaviate is running (docker-compose up -d) and your GEMINI_API_KEY is set.")
            return

    print("\nWelcome to the Intelligent Dialog System POC!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        try:
            response = process_query(user_input, collection_name)
            print(f"Agent: {response}")
        except Exception as e:
            print(f"Agent: An error occurred while processing your query: {e}")
            print("Please ensure Weaviate is running (docker-compose up -d) and data is ingested.")

if __name__ == "__main__":
    main()