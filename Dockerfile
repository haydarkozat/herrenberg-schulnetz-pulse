FROM python:3.10-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten zuerst kopieren (besseres Layer-Caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Restliche Anwendung kopieren
COPY . .

# FastAPI/Uvicorn Port
EXPOSE 8000

# Anwendung starten
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
