# src/rag_store.py
import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class StrategyStore:
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2', index_path='faiss_index.index', meta_path='strategy_metadata.pkl'):
        self.model = SentenceTransformer(embedding_model_name)
        self.index_path = index_path
        self.meta_path = meta_path
        self.index = faiss.IndexFlatL2(384)
        self.metadata = []

        if os.path.exists(index_path) and os.path.exists(meta_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, 'rb') as f:
                self.metadata = pickle.load(f)

    def add_strategy(self, summary_text, metadata):
        embedding = self.model.encode([summary_text])[0]
        self.index.add(np.array([embedding], dtype='float32'))
        self.metadata.append(metadata)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, 'wb') as f:
            pickle.dump(self.metadata, f)
