🚀 Quick Start

Follow these steps to quickly build and run the TTD service using Docker.

# Step 1: Step 1: Build & Start the Docker Container

Open a terminal and run:

```bash
cd ~/bioc/ttd_service
docker compose up --build
```

* This command will build the Docker image and start the TTD service container.

# Step 2: Access the Service

Once the container is running, the TTD API will be available at:

```bash
http://localhost:8012
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

