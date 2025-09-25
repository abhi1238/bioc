

# BioChirp

**BioChirp** is a next-generation, multi-agent biomedical conversational assistant for complex, citation-driven biological queries. It integrates multiple curated databases, advanced synonym and semantic search, and interpretable logic planning to answer biomedical questions about drugs, targets, genes, diseases, pathways, and more.

---

##  Features

- **Multi-Database Integration:**  
  Seamless querying across TTD, CTD, HCDT, and more.
- **Synonym Expansion & Fuzzy Matching:**  
  Expands biomedical entity names using domain knowledge and advanced embedding models (BioLORD, SapBERT, etc.).
- **Steiner-Tree Join Planning:**  
  Efficient cross-database joins for complex entity-relationship questions.
- **LLM-powered Multi-Agent Orchestration:**  
  Modular agents for query interpretation, validation, evidence retrieval, join/filtering, summarization, and memory recall.
- **Citation-Driven Answers:**  
  All outputs are sourced from trusted databases, with per-row citation and atomicity (no comma-separated facts).
- **Modern UI & API:**  
  FastAPI backend, Chainlit chat UI, CSV/Excel download, and structured JSON output.
- **Persistent Vector Search:**  
  Uses Qdrant for fast, filterable similarity search with persistent storage.
- **Evaluation & Benchmarking:**  
  Tools for comparing retrieval performance, citation coverage, and answer quality vs. other LLM chatbots.

---

