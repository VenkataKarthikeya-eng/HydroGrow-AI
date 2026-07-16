# HydroGrow AI — RAG Knowledge Subsystem

This subdirectory contains the lightweight local Retrieval-Augmented Generation (RAG) preparation subsystem for the HydroGrow AI agricultural assistant.

## Subsystem Architecture

The system operates locally without calling any heavy vector database engines or remote APIs. It flattens, tokenizes, indexes, and queries the agricultural database in milliseconds.

```
                  ┌──────────────────────────────┐
                  │ hydroponic_knowledge.json    │
                  └──────────────┬───────────────┘
                                 │ Load
                                 ▼
                    [ app/rag/knowledge_loader.py ]
                                 │
                                 ▼ (List of Document dicts)
                   [ app/rag/document_processor.py ]
                                 │
                                 ├─► splits into chunks
                                 ├─► normalizes tokens
                                 └─► builds inverted index
                                 │
                                 ▼
                        [ app/rag/retriever.py ]
                                 ▲
                                 │ query (str)
                                 ▼
                     Score via TF-IDF overlap
                                 │
                                 ▼ (Top-K Chunks)
                      ai_assistant.py Context
```

## Module Responsibilities

1. **`knowledge_loader.py`**:
   - Parses the structured `hydroponic_knowledge.json` configuration file.
   - Flattens optimal ranges, deficiencies, stages, mistakes, and guidelines into text documents tagged with source metadata tags.
2. **`document_processor.py`**:
   - Normalizes text by lowercasing and cleaning symbols/punctuation.
   - Chunks text into sliding-window records under 150 words.
   - Computes an inverted token-to-chunk index for fast keyword lookups.
3. **`retriever.py`**:
   - Calculates Inverse Document Frequency (IDF) weights for all vocabulary tokens.
   - Implements TF-IDF scoring of retrieved chunks.
   - Exposes a clean, independent wrapper function: `retrieve(query: str, top_k: int = 3) -> list[dict]`.

---

## Future LLM / Vector DB Integration Hooks

The retriever wrapper is intentionally decoupled from `ai_assistant.py` and `chat_interface.py` to facilitate seamless plug-and-play upgrades:

### 1. Swapping with a Vector Database (e.g. ChromaDB / FAISS)
To upgrade to a semantic vector store, modify `app/rag/retriever.py`:
```python
# app/rag/retriever.py (Future Upgrade)
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

client = PersistentClient(path="./chroma_db")
model = SentenceTransformer("all-MiniLM-L6-v2")
collection = client.get_or_create_collection("hydroponics")

def retrieve(query: str, top_k: int = 3) -> list[dict]:
    query_emb = model.encode(query).tolist()
    res = collection.query(query_embeddings=[query_emb], n_results=top_k)
    # Map res to [{"content": doc, "source": src, "score": d}]
    return formatted_results
```

### 2. Swapping with an LLM Generation Endpoint (e.g. OpenAI GPT-4o / Ollama Llama 3)
To feed RAG chunks into a generative model, modify the assistant response generator:
```python
# app/ai_assistant.py (Future LLM Integration)
import openai
from rag.retriever import retrieve

def generate_llm_response(query: str, context: dict) -> str:
    # 1. Fetch relevant agronomic chunks
    chunks = retrieve(query, top_k=3)
    
    # 2. Build LLM prompt combining chunks and user dashboard parameters
    prompt = f"Context: {context}\n\nRetrieved Chunks: {chunks}\n\nQuestion: {query}"
    
    # 3. Request LLM response
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```
No changes are required in `app.py` or `chat_interface.py` to enable this upgrade.
