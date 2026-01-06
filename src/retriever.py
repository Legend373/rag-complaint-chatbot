from sentence_transformers import SentenceTransformer
from src.vector_store import VectorStore

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.store = VectorStore()

    def retrieve(self, question, k=5):
        query_embedding = self.model.encode(
            [question],
            normalize_embeddings=True
        ).astype("float32")

        return self.store.search(query_embedding, k)
