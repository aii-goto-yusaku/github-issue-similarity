FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy project configuration
COPY pyproject.toml .

# Install dependencies using uv
RUN ~/.cargo/bin/uv pip install --no-cache .

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser
USER appuser

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]