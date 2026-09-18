# STREAMING_CHUNK:Configuring base Python environment image...
FROM python:3.11-slim

WORKDIR /app

# STREAMING_CHUNK:Installing dependencies...
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# STREAMING_CHUNK:Copying application source code and exposing port...
COPY . .

EXPOSE 8000

# STREAMING_CHUNK:Defining runtime container start command...
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]