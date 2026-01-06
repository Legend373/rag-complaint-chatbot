import pandas as pd
import pyarrow.parquet as pq
import faiss
import numpy as np
import pickle
from tqdm import tqdm
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

PARQUET_PATH = "vector_store/complaint_embeddings.parquet"
OUT_INDEX = "vector_store/task3_faiss.index"
OUT_META = "vector_store/task3_meta.pkl"

parquet_file = pq.ParquetFile(PARQUET_PATH)

print(parquet_file.schema)

index = None
metadata = []

print("Streaming parquet and building FAISS index...")

for batch in tqdm(parquet_file.iter_batches(batch_size=2048)):
    df = batch.to_pandas()

    # Stack embeddings
    emb = np.vstack(df["embedding"].values).astype("float32")

    # Initialize FAISS index once
    if index is None:
        dim = emb.shape[1]
        index = faiss.IndexFlatL2(dim)

    # Add vectors to FAISS
    index.add(emb)

    # Store metadata for each chunk
    for _, row in df.iterrows():
        metadata.append({
            "text": row["document"],
            "complaint_id": row["metadata"]["complaint_id"],
            "product": row["metadata"]["product"],
            "issue": row["metadata"]["issue"],
            "company": row["metadata"]["company"],
            "chunk_index": row["metadata"]["chunk_index"]
        })

# Save FAISS index
faiss.write_index(index, OUT_INDEX)

# Save metadata
with open(OUT_META, "wb") as f:
    pickle.dump(metadata, f)

print("FAISS index and metadata saved successfully!")
