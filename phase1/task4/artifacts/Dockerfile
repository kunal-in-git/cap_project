# Deployment artifact for Task D. Builds the real task1/backend app.
# Build from repo root with:
#   docker build -f phase1/task4/artifacts/Dockerfile -t task-manager-api phase1/task1/backend
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
