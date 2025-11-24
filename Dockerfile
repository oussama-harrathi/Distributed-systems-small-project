# Simple, one-stage image that includes deps
FROM python:3.13-slim

# Prevent pyc files and ensure unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY app/ ./app/

EXPOSE 8000

# Start the API
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
