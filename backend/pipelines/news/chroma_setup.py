import uuid
import chromadb


CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "signal_titles"

#creates and connect it to the local Chormadb
chromaClient = chromadb.PersistentClient(path=CHROMA_DB_PATH)

#craetes collection that stores title embeddings
collection = chromaClient.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)
