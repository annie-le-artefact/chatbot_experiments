import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType
import os

def test_weaviate_ingest_query():
    """
    Test script to ingest a chunk into Weaviate and query it back.
    """
    
    # Initialize Weaviate client
    # Option 1: Local instance
    client = weaviate.connect_to_local()
    
    # Option 2: Weaviate Cloud (uncomment and add your credentials)
    # client = weaviate.connect_to_weaviate_cloud(
    #     cluster_url="YOUR_CLUSTER_URL",
    #     auth_credentials=Auth.api_key("YOUR_API_KEY")
    # )
    
    try:
        # Define collection name
        collection_name = "TestChunks"
        
        # Create collection if it doesn't exist
        if not client.collections.exists(collection_name):
            client.collections.create(
                name=collection_name,
                vectorizer_config=Configure.Vectorizer.text2vec_transformers(),
                properties=[
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="source", data_type=DataType.TEXT),
                    Property(name="chunk_id", data_type=DataType.INT)
                ]
            )
            print(f"✓ Collection '{collection_name}' created")
        else:
            print(f"✓ Collection '{collection_name}' already exists")
        
        # Get the collection
        collection = client.collections.get(collection_name)
        
        # Test data - a chunk to ingest
        test_chunk = {
            "content": "Weaviate is an open-source vector database that allows you to store data objects and vector embeddings. It supports hybrid search combining vector and keyword search.",
            "source": "test_document.txt",
            "chunk_id": 1
        }
        
        # Ingest the chunk
        print("\n--- INGESTING CHUNK ---")
        uuid = collection.data.insert(
            properties={
                "content": test_chunk["content"],
                "source": test_chunk["source"],
                "chunk_id": test_chunk["chunk_id"]
            }
        )
        print(f"✓ Chunk ingested with UUID: {uuid}")
        print(f"  Content: {test_chunk['content'][:50]}...")
        
        # Query 1: Vector search (semantic search)
        print("\n--- QUERY 1: VECTOR SEARCH ---")
        query_text = "What is Weaviate and what can it do?"
        
        response = collection.query.near_text(
            query=query_text,
            limit=1
        )
        
        if response.objects:
            result = response.objects[0]
            print(f"Query: {query_text}")
            print(f"✓ Found result:")
            print(f"  UUID: {result.uuid}")
            print(f"  Content: {result.properties['content']}")
            print(f"  Source: {result.properties['source']}")
            print(f"  Chunk ID: {result.properties['chunk_id']}")
        else:
            print("✗ No results found")
        
        # Query 2: Keyword search (BM25)
        print("\n--- QUERY 2: KEYWORD SEARCH ---")
        keyword_query = "vector database"
        
        response = collection.query.bm25(
            query=keyword_query,
            limit=1
        )
        
        if response.objects:
            result = response.objects[0]
            print(f"Query: {keyword_query}")
            print(f"✓ Found result:")
            print(f"  Content: {result.properties['content'][:100]}...")
        else:
            print("✗ No results found")
        
        # Query 3: Hybrid search (combination of vector + keyword)
        print("\n--- QUERY 3: HYBRID SEARCH ---")
        
        response = collection.query.hybrid(
            query="open source vector search",
            limit=1
        )
        
        if response.objects:
            result = response.objects[0]
            print(f"Query: open source vector search")
            print(f"✓ Found result:")
            print(f"  Content: {result.properties['content'][:100]}...")
        else:
            print("✗ No results found")
        
        # Query 4: Get by UUID
        print("\n--- QUERY 4: GET BY UUID ---")
        result = collection.query.fetch_object_by_id(uuid)
        if result:
            print(f"✓ Retrieved object by UUID: {uuid}")
            print(f"  Content: {result.properties['content'][:50]}...")
        
        print("\n✓ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        raise
    
    finally:
        # Close the client connection
        client.close()
        print("\n✓ Client connection closed")

if __name__ == "__main__":
    print("=== WEAVIATE INGEST AND QUERY TEST ===\n")
    test_weaviate_ingest_query()