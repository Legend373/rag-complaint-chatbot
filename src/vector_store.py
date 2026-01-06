import faiss
import pickle
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

class VectorStore:
    def __init__(self):
        self.index = faiss.read_index("../vector_store/task3_faiss.index")
        with open("../vector_store/task3_meta.pkl", "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query_embedding, k=5):
        D, I = self.index.search(query_embedding, k)
        return [self.metadata[i] for i in I[0]]
