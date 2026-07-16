"""
document_processor.py — RAG Document Processor and Index Builder

Splits text documents into chunks, tokenizes and normalizes queries and documents,
and constructs a local inverted keyword search index for fast vector-less retrieval.
"""

import re

# Stop words to filter out during RAG tokenization to increase retrieval precision
STOP_WORDS = {
    "what", "is", "the", "on", "in", "at", "of", "and", "to", "a", "for", 
    "how", "do", "i", "about", "show", "me", "are", "you", "your", "my", 
    "with", "an", "this", "that", "it", "can", "should", "does", "did",
    "will", "would", "could", "from", "by", "or", "but", "if", "then"
}


def split_into_chunks(documents: list[dict], max_words: int = 150) -> list[dict]:
    """
    Splits documents into smaller chunks if word count exceeds max_words.
    Adds chunk_index metadata to each chunk record.
    """
    chunks = []
    for doc in documents:
        content = doc["content"]
        source = doc["source"]
        words = content.split()
        
        if len(words) <= max_words:
            chunks.append({
                "content": content,
                "source": source,
                "chunk_index": 0
            })
        else:
            for i in range(0, len(words), max_words):
                chunk_words = words[i:i + max_words]
                chunk_content = " ".join(chunk_words)
                chunks.append({
                    "content": chunk_content,
                    "source": source,
                    "chunk_index": i // max_words
                })
    return chunks


def normalize_text(text: str) -> list[str]:
    """
    Lowercases text, strips punctuation/special characters,
    filters out common stop words, and returns a clean list of tokens.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = [t for t in text.split() if t]
    return [t for t in tokens if t not in STOP_WORDS]


def build_inverted_index(chunks: list[dict]) -> dict[str, list[int]]:
    """
    Builds an inverted index mapping tokens (words) to chunk IDs (list indices).
    Used to accelerate keyword-matching during search.
    """
    inverted_index = {}
    for idx, chunk in enumerate(chunks):
        tokens = set(normalize_text(chunk["content"]))
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = []
            inverted_index[token].append(idx)
    return inverted_index
