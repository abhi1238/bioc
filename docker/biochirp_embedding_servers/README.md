# BioChirp Embedding Server

A production-ready FastAPI server for biomedical SentenceTransformer models, served as REST APIs in Docker containers.

## 🚀 Quick Start

Open a terminal and run:

### Step 1: Build the Docker Image

```bash
cd ~/bioc/docker/biochirp_embedding_servers
docker build -t biochirp_embedding_server .
```

### Step 2: Run the Embedding Server

You can run individual embedding servers, or all servers at once.

#### **Option A: Run a Single Embedding Server**

##### 1. Foreground Mode (default, shows logs)

```bash
docker compose -f docker-compose-biochirp_wikimedical.yml up
docker compose -f docker-compose-biochirp_scincl.yml up
docker compose -f docker-compose-biochirp_sapbert.yml up
docker compose -f docker-compose-biochirp_pubmedbert.yml up
docker compose -f docker-compose-biochirp_biolord.yml up

```
* This will start each container and show logs in your terminal.

* Do not close the terminal while the server is running.

* To stop the server, use Ctrl+C.


##### 2. Detached Mode (optional, runs in background)

If you want to run any server in the background (no logs in terminal), add -d:

```bash
docker compose -f docker-compose-biochirp_wikimedical.yml up -d
docker compose -f docker-compose-biochirp_scincl.yml up -d
docker compose -f docker-compose-biochirp_sapbert.yml up -d
docker compose -f docker-compose-biochirp_pubmedbert.yml up -d
docker compose -f docker-compose-biochirp_biolord.yml up -d
```
* The containers will keep running in the background.

* To stop a detached container, run:

```bash
docker compose -f docker-compose-biochirp_wikimedical.yml down

```

#### **Option B: Run All Embedding Servers Together (Recommended)**

Run all models in one go (best for full deployment/benchmarking):

```bash
docker compose -f docker-compose.biochirp_all.yml up
```

Shows logs for all servers in one terminal.
Stop all servers with Ctrl+C.


* To run in background (detached mode):
```bash
docker compose -f docker-compose.biochirp_all.yml up -d
```

* To run in background (detached mode):

```bash
docker compose -f docker-compose.biochirp_all.yml up -d
```

* Stop with:

```bash
docker compose -f docker-compose.biochirp_all.yml down
```




