FROM python:3.11-slim

WORKDIR /app
COPY ./app /app/app

COPY ./data /app/data
COPY requirements.txt /app/requirements.txt
# RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir -i https://pypi.org/simple -r /app/requirements.txt

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8013"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8013"]

