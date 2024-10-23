FROM python:3.11-slim

WORKDIR /app

# Create non-root user and required directories
RUN useradd -m appuser && \
    mkdir -p /app/logs && \
    mkdir -p /cache && \
    chown -R appuser:appuser /app /cache

# Update apt keys and install system dependencies
RUN rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends gnupg2 && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Switch to non-root user
USER appuser

# Set environment variables for huggingface
ENV TRANSFORMERS_CACHE=/cache \
    HF_HOME=/cache

# Install uv for the appuser
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy all application code
COPY --chown=appuser:appuser . .

# Create virtual environment and install dependencies
RUN ~/.cargo/bin/uv venv && \
    . .venv/bin/activate && \
    ~/.cargo/bin/uv pip install .

# Create healthcheck script
RUN printf '#!/bin/sh\ncurl -s -f http://localhost:8000/health | grep -q "status.*healthy" || exit 1\n' > /app/scripts/healthcheck.sh && \
    chmod +x /app/scripts/healthcheck.sh

# Run the application with virtual environment
CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use HEALTHCHECK instruction
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /app/scripts/healthcheck.sh