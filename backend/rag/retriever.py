"""
retriever.py — Modular RAG Knowledge Retriever

This module provides a modular knowledge retrieval layer. It scores chunks using TF-IDF-based keyword overlap,
measures execution speed, and exposes a clean interface that can be replaced with FAISS or ChromaDB in the future.
"""

import sys
import os
import math
import time

# Ensure directory is in Python path for local imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from knowledge_loader import load_knowledge_base
from document_processor import split_into_chunks, build_inverted_index, normalize_text
from backend.rag.query_processor import QueryProcessor
from backend.rag.document_ranker import DocumentRanker


class LocalRetriever:
    """
    A lightweight, vector-less local retriever that parses questions
    and retrieves relevant hydroponic knowledge in under 1 second.
    """
    def __init__(self):
        # 1. Load document database
        self.docs = load_knowledge_base()
        # 2. Chunk documents
        self.chunks = split_into_chunks(self.docs)
        # 3. Build inverted keyword search index
        self.inverted_index = build_inverted_index(self.chunks)
        self.total_chunks = len(self.chunks)
        
        # 4. Compute Inverse Document Frequency (IDF) for each word
        self.idf = {}
        for token, chunk_ids in self.inverted_index.items():
            # Standard IDF formula with smoothing to avoid division by zero
            self.idf[token] = math.log(1.0 + (self.total_chunks / (len(chunk_ids) + 1.0)))

    def retrieve(self, query: str, top_k: int = 3, intent: Optional[str] = None) -> list[dict]:
        """
        Retrieves the top-k most relevant knowledge chunks based on query tokens.
        Each returned dict matches: {"content": str, "source": str, "score": float}
        """
        start_time = time.time()
        
        # Conditionally expand query based on intent
        processed_query = query
        if intent and intent != "fallback":
            processed_query = QueryProcessor.expand_query(query, intent)

        query_tokens = normalize_text(processed_query)
        
        # Track matching tokens per chunk ID
        chunk_matches = {}
        for token in query_tokens:
            if token in self.inverted_index:
                for chunk_id in self.inverted_index[token]:
                    if chunk_id not in chunk_matches:
                        chunk_matches[chunk_id] = set()
                    chunk_matches[chunk_id].add(token)
                    
        scores = {}
        for chunk_id, matched_tokens in chunk_matches.items():
            # Heuristic: If user query contains multiple keywords (after stop words filtering),
            # require that at least 2 distinct keywords match to prevent irrelevant single-word hits.
            if len(query_tokens) >= 2 and len(matched_tokens) < 2:
                continue
                
            chunk_content = self.chunks[chunk_id]["content"]
            chunk_words = normalize_text(chunk_content)
            
            chunk_score = 0.0
            for token in matched_tokens:
                # Raw count TF (frequency) - rewards documents that mention the topic multiple times
                tf = chunk_words.count(token)
                idf_val = self.idf.get(token, 0.0)
                chunk_score += tf * idf_val
                
            scores[chunk_id] = chunk_score
            
        results = []
        for chunk_id, score in scores.items():
            chunk = self.chunks[chunk_id]
            results.append({
                "content": chunk["content"],
                "source": chunk["source"],
                "score": score
            })
            
        # Rerank matching documents
        ranked = DocumentRanker.rank_documents(results)
        
        retrieval_time = time.time() - start_time
        # print(f"[INFO] Retrieval completed in {retrieval_time * 1000:.2f} ms")
        
        return ranked[:top_k]


# Global singleton instance
_retriever_instance = None


def retrieve(query: str, top_k: int = 3, intent: Optional[str] = None) -> list[dict]:
    """
    Independent wrapper function for knowledge retrieval.
    Allows easy future replacement with vector DB backends (FAISS, ChromaDB, etc.)
    without changing the assistant interface.
    """
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = LocalRetriever()
        
    return _retriever_instance.retrieve(query, top_k=top_k, intent=intent)


if __name__ == "__main__":
    test_query = "calcium deficiency tip burn"
    print(f"Testing retriever with query: '{test_query}'")
    matches = retrieve(test_query, top_k=2)
    for idx, match in enumerate(matches, 1):
        print(f"\nMatch {idx} [Score: {match['score']:.4f}] from '{match['source']}':")
        print(f"Content: {match['content']}")
