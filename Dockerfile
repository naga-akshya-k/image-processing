# Production Dockerfile for PCB AI Inspection System Engine
# Optimized for Cloud Platforms (Render, Railway, Hugging Face, Fly.io, Cloud Run)
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for OpenCV and healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Optimize PyTorch: pre-install CPU-only wheels to reduce image size and build time
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Copy requirements and install remaining dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Default port (Render/Railway/Cloud Run override this dynamically via $PORT)
ENV PORT=8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start Uvicorn dynamically bound to $PORT
CMD ["sh", "-c", "python -m uvicorn server.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
