

## 🚀 Quick Start

Open a terminal and run:

### Step 1: Change directory

```bash
cd ~/bioc/app/tools/interpreter_agent
```

### Step 2: Run Options (choose one)

* Foreground mode (runs in your terminal; logs visible; stops when you hit Ctrl+C):

```bash
docker compose up --build
```

* Detached mode (runs in background; use docker compose logs / docker compose down to manage):

```bash
docker compose up --build -d
```

* The service will listen on port 8016, so you can access it at: [Link](http://192.168.22.20:8016)


### To stop and remove containers, run:

```bash
docker compose down
```