FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn sentence-transformers

COPY serve_model.py .

EXPOSE 8005

CMD ["uvicorn", "serve_model:app", "--host", "0.0.0.0", "--port", "8005"]
