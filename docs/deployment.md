# Deployment Guide

This guide covers different deployment options for the GitHub Issue Similarity Detector.

## Table of Contents

- [Docker Deployment](#docker-deployment)
- [Systemd Service Deployment](#systemd-service-deployment)
- [Cloud Platform Deployment](#cloud-platform-deployment)
- [Production Considerations](#production-considerations)

## Docker Deployment

### 1. Create Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
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
```

### 2. Create Docker Compose file

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - GITHUB_REPO=${GITHUB_REPO}
      - SIMILARITY_THRESHOLD=${SIMILARITY_THRESHOLD}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 3. Deploy with Docker

```bash
# Build and start the container
docker-compose up -d

# Check logs
docker-compose logs -f

# Update deployment
docker-compose pull
docker-compose up -d
```

## Systemd Service Deployment

### 1. Create Virtual Environment

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Create and activate virtual environment
cd /opt/github-issue-similarity
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install --no-cache .
```

### 2. Create Systemd Service

Create `/etc/systemd/system/github-issue-similarity.service`:

```ini
[Unit]
Description=GitHub Issue Similarity Detector
After=network.target

[Service]
Type=simple
User=github-bot
Group=github-bot
WorkingDirectory=/opt/github-issue-similarity
Environment="GITHUB_TOKEN=your_token"
Environment="GITHUB_REPO=owner/repo"
Environment="SIMILARITY_THRESHOLD=0.8"
ExecStart=/opt/github-issue-similarity/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 3. Start and Enable Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start github-issue-similarity

# Enable on boot
sudo systemctl enable github-issue-similarity

# Check status
sudo systemctl status github-issue-similarity
```

## Cloud Platform Deployment

### Google Cloud Run

1. Build and push container:
```bash
gcloud builds submit --tag gcr.io/your-project/github-issue-similarity
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy github-issue-similarity \
  --image gcr.io/your-project/github-issue-similarity \
  --platform managed \
  --allow-unauthenticated
```

### Heroku

1. Create Procfile:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Deploy:
```bash
heroku create
git push heroku main
```

## Production Considerations

### Security

1. **SSL/TLS**
   - Use HTTPS for webhook endpoints
   - Set up SSL certificates (Let's Encrypt)
   - Configure secure headers

2. **Environment Variables**
   - Use secure secrets management
   - Rotate credentials regularly
   - Limit access to production secrets

### Monitoring

1. **Application Health Monitoring**
   - Use the built-in health check endpoint:
     ```bash
     curl http://your-server:8000/health
     ```
   - Monitor the response for:
     - Overall system status
     - GitHub API connectivity
     - Token validity
     - Rate limit information
     - Model status
   - Set up automated health checks (e.g., Pingdom, UptimeRobot)
   - Configure alerts for health status changes

2. **Application Monitoring**
   - Set up logging (e.g., CloudWatch, Stackdriver)
   - Configure error tracking (e.g., Sentry)
   - Monitor application metrics

2. **System Monitoring**
   - CPU and memory usage
   - Network traffic
   - Disk usage

### High Availability

1. **Load Balancing**
   - Set up multiple application instances
   - Use a load balancer (e.g., Nginx)
   - Configure health checks

2. **Backup and Recovery**
   - Regular backups of configuration
   - Documented recovery procedures
   - Failover testing

### Performance

1. **Caching**
   - Cache similarity calculations
   - Use Redis for temporary storage
   - Implement rate limiting

2. **Database Optimization**
   - Index frequently queried fields
   - Regular maintenance
   - Query optimization

### Scaling

1. **Horizontal Scaling**
   - Container orchestration (Kubernetes)
   - Auto-scaling policies
   - Load testing

2. **Resource Management**
   - Memory limits
   - CPU allocation
   - Disk space monitoring

## Maintenance

### Updates

1. Regular updates:
```bash
# Pull latest changes
git pull origin main

# Update dependencies
uv pip install --no-cache -U .

# Restart service
sudo systemctl restart github-issue-similarity
```

### Backup

1. Configuration backup:
```bash
# Backup env files
cp .env .env.backup

# Backup systemd service file
sudo cp /etc/systemd/system/github-issue-similarity.service /etc/systemd/system/github-issue-similarity.service.backup
```

### Logging

Configure logging in `app/main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/github-issue-similarity/app.log'),
        logging.StreamHandler()
    ]
)
```

## Troubleshooting

### Common Issues

1. **Service not starting**
   - Check logs: `journalctl -u github-issue-similarity`
   - Verify permissions
   - Check environment variables

2. **Memory issues**
   - Monitor memory usage
   - Adjust container limits
   - Check for memory leaks

3. **Network issues**
   - Verify firewall rules
   - Check DNS resolution
   - Test network connectivity