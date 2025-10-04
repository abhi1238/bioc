

## 🚀 Quick Start: Readme Agent

Get your BioChirp Readme Agent running in just a few steps.

### Step 1: Change directory

```bash
cd ~/bioc/app/tools/readme
```

### Step 2: Start the Service (Choose One Option)

* A. Foreground mode (runs in your terminal; logs visible; stops when you hit Ctrl+C):

```bash
docker compose up --build
```

* B. Detached mode (runs in background; use docker compose logs / docker compose down to manage):

```bash
docker compose up --build -d
```

### Step 3: Access the Readme Agent

* Once running, the service will be available at: [Link](http://192.168.22.20:8017)


### Step 4: Stop & Remove Containers

```bash
docker compose down
```

### API Documentation

For interactive API docs and to test endpoints in your browser, visit: [Link](http://192.168.22.20:8017/docs)

<!-- ![alt text](image.png) -->