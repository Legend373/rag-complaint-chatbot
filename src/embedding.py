import pandas as pd
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os

class Embedder:
    def __init__(self, df: pd.DataFrame, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        df: cleaned DataFrame with columns 'cleaned_narrative', 'Complaint ID', 'Product'
        model_name: embedding model
        """
        self.df = df
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.metadata = []

    def stratified_sample(self, n_samples=12000, seed=42):
        """Create stratified sample across products"""
        sampled = (
            self.df.groupby('Product', group_keys=False)
            .apply(lambda x: x.sample(frac=n_samples/len(self.df), random_state=seed))
        )
        self.df = sampled.reset_index(drop=True)
        return self

    def chunk_texts(self, chunk_size=500, chunk_overlap=50):
        """Split long narratives into chunks"""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?"]
        )
        for _, row in tqdm(self.df.iterrows(), total=len(self.df), desc="Chunking"):
            text = row['cleaned_narrative']
            chunks = splitter.split_text(text)
            for chunk in chunks:
                self.chunks.append(chunk)
                self.metadata.append({
                    "complaint_id": row['Complaint ID'],
                    "product": row['Product']
                })
        return self

    def embed_chunks(self):
        """Generate embeddings for all chunks"""
        print("Generating embeddings...")
        embeddings = self.model.encode(self.chunks, show_progress_bar=True)
        self.embeddings = embeddings.astype("float32")  # FAISS requires float32
        return self

    def create_faiss_index(self, index_path="vector_store/faiss_index"):
     """
     Saves FAISS index and metadata to disk
     """
     # Ensure parent directory exists
     base_dir = os.path.dirname(index_path)
     os.makedirs(base_dir, exist_ok=True)

     # Create FAISS index
     dim = self.embeddings.shape[1]
     index = faiss.IndexFlatL2(dim)
     index.add(self.embeddings)

     # Save index
     faiss.write_index(index, f"{index_path}.index")

     # Save metadata
     with open(f"{index_path}_metadata.pkl", "wb") as f:
        pickle.dump(self.metadata, f)

     print(f"FAISS index saved to {index_path}.index")