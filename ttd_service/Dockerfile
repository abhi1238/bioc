FROM python:3.11-slim

WORKDIR /app

# Copy app code
COPY ./app /app/app

# Copy data folder (must exist!)
COPY ./data /app/data

# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8012"]
