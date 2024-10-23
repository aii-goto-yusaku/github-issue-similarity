FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Create non-root user and required directories
RUN useradd -m appuser && \
    mkdir -p /app/logs && \
    chown -R appuser:appuser /app

# Copy project configuration
COPY --chown=appuser:appuser pyproject.toml .

# Switch to non-root user for dependency installation
USER appuser

# Install dependencies using uv (without --no-cache for better build caching)
RUN ~/.cargo/bin/uv pip install .

# Copy application code
COPY --chown=appuser:appuser . .

# Create directory for health check script
RUN mkdir -p /app/scripts

# Create health check script
RUN echo '#!/bin/sh\n\
curl -s -f http://localhost:8000/health | grep -q \'"status": "healthy"\' || exit 1' > /app/scripts/healthcheck.sh && \
    chmod +x /app/scripts/healthcheck.sh

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use HEALTHCHECK instruction instead of docker-compose healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD /app/scripts/healthcheck.sh