
FROM python:3.11-slim

WORKDIR /app

# Copy the code from local `app/` folder into /app 
COPY ./app /app

# Copy data (if needed)
COPY ./data /data

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -i https://pypi.org/simple -r /app/requirements.txt
# Expose API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8012"]
