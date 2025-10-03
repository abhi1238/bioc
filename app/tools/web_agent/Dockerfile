FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first (use Docker layer caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code *after* installing dependencies
COPY . .

# Expose the port your app will run on
EXPOSE 8015

# Use 'exec' form for CMD (so signals are handled correctly)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8015s"]
