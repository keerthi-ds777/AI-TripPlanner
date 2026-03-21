# ==========================================
# AI Travel Planner - Dockerfile
# ==========================================
# Build from project root: docker build -f Docker/Dockerfile -t ai-tripplanner .

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Docker-specific requirements (excludes Windows packages)
COPY requirements.docker.txt .
RUN pip install uv
# Install Python dependencies (--system since no venv in Docker)
RUN uv pip install --system --no-cache-dir -r requirements.docker.txt

# Copy project files
COPY . .

# Install the package in editable mode (for setup.py)
RUN pip install -e .

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Default command: Run FastAPI backend (main.py is in app folder)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
