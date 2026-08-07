# Use an official, lightweight Python base image
FROM python:3.11-slim

# Set environment paths and behaviors
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establish the working directory inside the container runtime context
WORKDIR /app

# Install native system dependencies required for building C extensions (like psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency manifest first to take advantage of Docker build layer caching
COPY requirements.txt /app/

# Install Python packages smoothly
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the entire backend application codebase into the active image workspace
COPY ./backend /app/backend

# Expose the internal port that your FastAPI application binds to
EXPOSE 8000

# Fire up the production ASGI server instance mapping execution entry points
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]