
# BioChirp

**BioChirp** is a next-generation, multi-agent biomedical conversational assistant for complex, citation-driven biological queries. It integrates multiple curated databases, advanced synonym and semantic search, and interpretable logic planning to answer biomedical questions about drugs, targets, genes, diseases, pathways, and more.


🚀 Quick Start

Open a terminal and run:

## Step 1: Build the Docker Image for transformer models

```bash
cd ~/bioc/docker/biochirp_embedding_servers
docker build -t biochirp_embedding_server .
```
## Step 2: Run all the Embedding Servers/ transformers at once

Run all models in one go (best for full deployment/benchmarking):

```bash
cd ~/bioc/docker/biochirp_embedding_servers
docker compose -f docker-compose.biochirp_all.yml up
```

