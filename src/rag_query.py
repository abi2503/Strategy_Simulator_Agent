# src/rag_query.py
"""
This module retrieves similar strategies from a stored FAISS vector index using a new strategy summary.
"""
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class StrategyRetriever:
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2', index_path='faiss_index.index', meta_path='strategy_metadata.pkl'):
        self.model = SentenceTransformer(embedding_model_name)
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'rb') as f:
            self.metadata = pickle.load(f)

    def query(self, new_summary_text, top_k=3):
        """
        Embed the new summary and return top_k similar strategy metadata.
        """
        query_vec = self.model.encode([new_summary_text])[0].astype('float32')
        distances, indices = self.index.search(np.array([query_vec]), top_k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                results.append({
                    "similarity": float(1 - dist),  # convert L2 distance to similarity-like score
                    "metadata": self.metadata[idx]
                })
        return results

# Example usage
if __name__ == "__main__":
    retriever = StrategyRetriever()
    new_summary = """
    This strategy combines an Alpha signal with a Hedge overlay. It spans 2009 to 2019 and yields a total return near 40%.
    It aims to reduce market exposure while maintaining edge from a predictive alpha model.
    """
    results = retriever.query(new_summary)
    for res in results:
        print("Similarity:", res['similarity'])
        print("Match:", res['metadata'])
        print("-")
