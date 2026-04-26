import uuid
import chromadb

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "signal_titles"

#creates and connect it to the local Chormadb
chromaClient = chromadb.PersistentClient(path=CHROMA_DB_PATH)

#creates collection that stores title embeddings
collection = chromaClient.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

def querySimilarTitle(embedding, threshold: float = 0.77):

    #find the most similar saved title to this new title embedding
    results = collection.query(
        queryEmbeddings=[embedding],
        nRes=1
    )

    # if not results["ids"] or not results["ids"][0]:
    #     return None

    # get closest match distance and metadata
    distance = results["distances"][0][0]
    metaData = results["metadatas"][0][0]

    #cosine distance (lower = closer) into similarity (higher = more similar)
    similarity = 1 - distance

    if similarity >= threshold:
        return metaData.get("group_key")

    return None

# def storeTitleEmbedding(item, title: str, embedding, group_key: str):
#     signalId = str(uuid.uuid4())

#     collection.add(
#         ids=[signalId],
#         embeddings=[embedding],
#         documents=[title],
#         metaDatas=[{
#             "group_key": group_key,
#             "title": item.get("title", ""),
#             "source": item.get("source", ""),
#             "url": item.get("url", ""),
#             "category": item.get("category", ""),
#             "fetched_at": item.get("fetched_at", "")
#         }]
#     )