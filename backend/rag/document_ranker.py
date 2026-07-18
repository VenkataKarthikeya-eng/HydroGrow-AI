from typing import List, Dict, Any

class DocumentRanker:
    """
    Reranks and filters RAG document chunks to ensure high precision context integration.
    """
    @staticmethod
    def rank_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Sort documents by score descending (stability check)
        return sorted(documents, key=lambda d: d.get("score", 0.0), reverse=True)

    @staticmethod
    def filter_relevant_context(
        documents: List[Dict[str, Any]], 
        min_threshold: float = 0.08
    ) -> List[Dict[str, Any]]:
        # Filters out any RAG matches that fall below the relevance threshold
        return [d for d in documents if d.get("score", 0.0) >= min_threshold]
