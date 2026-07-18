# HydroGrow AI Knowledge Intelligence & RAG Pipeline

Pipeline architecture integrating agronomic research, knowledge search, recommendation synthesis, and conversational AI.

---

## 1. Intelligence Pipeline Flow

```mermaid
graph TD
    UserQuery[User Query e.g. How to improve lettuce yield?] --> KnowledgeEngine[Knowledge Engine & RAG Index]
    KnowledgeEngine --> RecEngine[Global Recommendation Engine]
    RecEngine --> Assistant[HydroGrow Conversational AI Assistant]
    Assistant --> Response[Contextual Markdown Diagnostic Response]
```
