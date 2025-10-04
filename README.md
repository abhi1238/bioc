
# BioChirp

**BioChirp** is a next-generation, multi-agent biomedical conversational assistant for complex, citation-driven biological queries. It integrates multiple curated databases, advanced synonym and semantic search, and interpretable logic planning to answer biomedical questions about drugs, targets, genes, diseases, pathways, and more.


## 🚀 Quick Start

Open a terminal and run:

### Step 1: Build the Docker Image for transformer models.

```bash
cd ~/bioc/docker/biochirp_embedding_servers
docker build -t biochirp_embedding_server .
```
### Step 2: Run all the Embedding Servers/ all transformer models at once.

Run all models in one go (best for full deployment/benchmarking):

```bash
cd ~/bioc/docker/biochirp_embedding_servers
docker compose -f docker-compose.biochirp_all.yml up
```


### Step 3: Build the Docker Image for TTD service.


Open a terminal and run:

```bash
cd ~/bioc/ttd_service
docker compose up --build
```

* This command will build the Docker image and start the TTD service container.


### Step 4: Build the Docker Image for CTD service.


Open a terminal and run:

```bash
cd ~/bioc/ctd_service
docker compose up --build
```

* This command will build the Docker image and start the CTD service container.



### Step 5: Build the Docker Image for HCDT service.


Open a terminal and run:

```bash
cd ~/bioc/hcdt_service
docker compose up --build
```

* This command will build the Docker image and start the HCDT service container.


### Step 6: Build and Run the Web Search Tool Docker Service
```bash
cd ~/bioc/app/tools/web_agent
docker compose up --build
```

* The service will listen on port 8015, so you can access it at: [Link](http://192.168.22.20:8015)

⚠️
❌
✅
🚀
