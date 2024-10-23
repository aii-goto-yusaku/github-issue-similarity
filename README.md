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

1. Clone the repository:
```bash
git clone https://github.com/aii-goto-yusaku/github-issue-similarity.git
cd github-issue-similarity
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Create a `.env` file with the following variables:

```env
GITHUB_TOKEN=your_github_token
GITHUB_REPO=owner/repo
SIMILARITY_THRESHOLD=0.8  # Minimum similarity score (0.0 to 1.0)
```

## Usage

1. Start the webhook server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. Configure GitHub webhook:
   - Go to your repository settings
   - Add webhook with URL: `http://your-server:8000/webhook`
   - Select content type: `application/json`
   - Choose "Issues" events

The system will now automatically analyze new issues and comment when similar issues are found.

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
