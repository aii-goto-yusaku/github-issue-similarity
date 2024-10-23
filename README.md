# GitHub Issue Similarity Detector

A system that automatically detects similar issues and provides recommendations for duplicate GitHub issues using natural language processing. When a new issue is created, the system analyzes its content and compares it with existing issues, then adds a comment with links to similar issues if found.

## Features

- 🔍 Automatic similarity detection for new issues
- 🤖 Bot comments with links to similar issues
- 🌐 Multi-language support (English & Japanese) using multilingual embeddings
- ⚙️ Configurable similarity threshold
- 🔒 Secure GitHub integration

## System Requirements

- Python 3.11+
- PostgreSQL (optional, for caching)
- GitHub repository with Issues enabled
- GitHub Personal Access Token with repo scope

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

If you don't have uv installed, our setup script will install it for you.

### Setup

1. Clone the repository:
```bash
git clone https://github.com/aii-goto-yusaku/github-issue-similarity.git
cd github-issue-similarity
```

2. Run the setup script:
```bash
./scripts/setup-dev.sh
```

This will:
- Install uv if not present
- Create a virtual environment
- Install all dependencies including development tools

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Manual Setup (Alternative)

If you prefer to set up manually:

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install --no-cache -e ".[dev]"
```

## Configuration

Create a `.env` file with the following variables:

```env
GITHUB_TOKEN=your_github_token
GITHUB_REPO=owner/repo
SIMILARITY_THRESHOLD=0.8  # Minimum similarity score (0.0 to 1.0)
```

## Usage

### Local Development

1. Start the webhook server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Production Deployment

For production deployment options, including:
- Docker deployment
- Systemd service
- Cloud platforms (Google Cloud Run, Heroku)
- Security considerations
- Monitoring setup

Please refer to our comprehensive [Deployment Guide](docs/deployment.md)

2. Configure GitHub webhook:
   - Follow the [detailed webhook setup guide](docs/webhook-setup.md)
   - Or quickly configure with these basic settings:
     - URL: `http://your-server:8000/webhook`
     - Content type: `application/json`
     - Events: "Issues" only

The system will now automatically analyze new issues and comment when similar issues are found.

For security considerations and advanced configuration options, please refer to the [webhook setup guide](docs/webhook-setup.md).

## How it Works

1. When a new issue is created, GitHub sends a webhook event to the server
2. The system extracts the issue title and body
3. Using Sentence Transformers, it converts the text into embeddings
4. Compares the embeddings with existing issues using cosine similarity
5. If similar issues are found (similarity > threshold), posts a comment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details
