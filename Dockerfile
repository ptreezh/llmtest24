FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt requirements-dev.txt requirements-optional.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install optional dependencies
RUN pip install --no-cache-dir -r requirements-optional.txt

# Copy project files
COPY . .

# Create virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Create directories
RUN mkdir -p testout results test_logs memory_db docs/build examples

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create a user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port for web interface
EXPOSE 8501

# Default command
CMD ["python", "visual_test_interface.py"]
