from qdrant_client import QdrantClient, models
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import uuid
import qdrant_client as _qc


# Load GEMINI key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env")

# initialize google/gemini embeddings
emb = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GEMINI_API_KEY)
model_name = "models/text-embedding-004"

# running qdrant in local mode suitable for experiments
client = QdrantClient(":memory:")  # or QdrantClient(path="path/to/db") for local mode and persistent storage

payload = [
    {"document": "The Danish Working Environment Authority has the task of guiding undertakings, sector partnerships for the working environment, labour market organisations, employees, other target groups and the public on working environment issues, providing undertakings with 1-4 employees with further guidance, assisting the Ministry of Employment with the preparation of rules, issuing regulations pursuant to authorisation from the Minister for Employment, keeping informed of technical and social developments with a view to improving work for safety and health, processing plans for work processes, workplaces, technical equipment, etc., as well as substances and materials and granting permits, and ensuring that the Act and the regulations issued under the Act are complied with.", "source": "DK-LEGAL_DOCUMENTS-2025-1108_en.txt"},
]

# compute embeddings with Google and prepare points
points = []
for p in payload:
    vector = emb.embed_query(p["document"])
    points.append(models.PointStruct(id=str(uuid.uuid4()), vector=vector, payload=p))

embedding_size = len(points[0].vector)

try:
    client.delete_collection(collection_name="demo_collection")
except Exception:
    pass

client.create_collection(
    collection_name="demo_collection",
    vectors_config=models.VectorParams(size=embedding_size, distance=models.Distance.COSINE),
)

# upload via upsert (widely supported) — simple and explicit
client.upsert(collection_name="demo_collection", points=points)

# query using a Google-generated vector
# keep a vector locally (not used by query_points for 1.16.x)
q_vec = emb.embed_query("safety and health measures concerning works")

# detect qdrant-client version
search_result = client.query_points(
    collection_name="demo_collection",
    query=q_vec
).points

print(search_result)
