# FROM python:3.11-slim

# WORKDIR /app

# # Copy app code
# COPY ./app /app

# COPY ./data /data

# # Copy requirements
# COPY requirements.txt requirements.txt

# # Install dependencies
# # RUN pip install --no-cache-dir -r /app/requirements.txt
# RUN pip install --no-cache-dir -i https://pypi.org/simple -r requirements.txt


# # Expose API
# CMD ["uvicorn", "app.main", "--host", "0.0.0.0", "--port", "8014"]

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

# Run Uvicorn with correct module path
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8014"]
