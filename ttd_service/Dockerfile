FROM python:3.11-slim

WORKDIR /app
COPY ./app /app/app
COPY ../common_utils /app/common_utils
COPY ./data /app/data
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8012"]


