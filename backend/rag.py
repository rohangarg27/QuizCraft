import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

INDEX_PATH = "storage/faiss.index"
META_PATH = "storage/metadata.pkl"

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    return " ".join(page.extract_text() or "" for page in reader.pages)

def chunk_text(text: str, chunk_size: int = 500) -> list:
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def build_faiss_index(chunks: list):
    os.makedirs("storage", exist_ok=True)
    vectors = embedder.encode(chunks, convert_to_numpy=True)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)

def retrieve_chunks(query: str, top_k: int = 3):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        chunks = pickle.load(f)
    query_vec = embedder.encode([query], convert_to_numpy=True)
    _, idx = index.search(query_vec, top_k)
    return [chunks[i] for i in idx[0]]
