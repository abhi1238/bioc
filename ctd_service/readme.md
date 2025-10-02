# 🚀  Quick Start

Follow these steps to quickly build and run the CTD service using Docker.

## Step 1: Step 1: Build & Start the Docker Container

Open a terminal and run:

```bash
cd ~/bioc/ctd_service
docker compose up --build
```

* This command will build the Docker image and start the CTD service container.

## Step 2: Access the Service

Once the container is running, the CTD API will be available at:

```bash
http://localhost:8013
```

You can verify its running by opening the above URL in your browser, or with:

# Tip:

To run the service in the background (detached mode), use:
```bash
docker compose up --build -d
```

To stop the service, press <kbd>Ctrl+C</kbd> (if running in the foreground) or:
```bash
docker compose down
```

