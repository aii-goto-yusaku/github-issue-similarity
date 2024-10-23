from github import Github
from github.GithubException import BadCredentialsException, UnknownObjectException
from typing import List, Tuple, Optional

class GitHubConfigError(Exception):
    """Raised when there are configuration issues with GitHub setup."""
    pass

class GitHubService:
    def __init__(self, token: Optional[str], repo_name: Optional[str]):
        """Initialize GitHub service with token and repository name."""
        if not token:
            raise GitHubConfigError(
                "GitHub token is not configured. "
                "Please set the GITHUB_TOKEN environment variable with a valid token. "
                "You can create one at: https://github.com/settings/tokens"
            )
        if not repo_name:
            raise GitHubConfigError(
                "GitHub repository is not configured. "
                "Please set the GITHUB_REPO environment variable in the format 'owner/repo'"
            )
        
        try:
            self.github = Github(token)
            # Test the token by making a simple API call
            self.github.get_user().login
        except BadCredentialsException:
            raise GitHubConfigError(
                "Invalid GitHub token. "
                "Please check your GITHUB_TOKEN environment variable and ensure it has the required permissions. "
                "You can create a new token at: https://github.com/settings/tokens"
            )
        
        try:
            self.repo = self.github.get_repo(repo_name)
        except UnknownObjectException:
            raise GitHubConfigError(
                f"Repository '{repo_name}' not found or not accessible. "
                "Please check your GITHUB_REPO environment variable and ensure it's in the format 'owner/repo' "
                "and that your token has access to this repository."
            )
    
    def get_open_issues(self) -> List[dict]:
        """オープン状態のIssueを取得"""
        issues = []
        for issue in self.repo.get_issues(state='open'):
            issues.append({
                'number': issue.number,
                'title': issue.title,
                'body': issue.body or '',
                'created_at': issue.created_at
            })
        return issues
    
    def add_comment(self, issue_number: int, comment: str) -> None:
        """Issueにコメントを追加"""
        issue = self.repo.get_issue(number=issue_number)
        issue.create_comment(comment)
    
    def check_connection(self) -> dict:
        """GitHubとの接続状態を確認"""
        try:
            user = self.github.get_user().login
            repo = self.repo.full_name
            return {
                "status": "healthy",
                "github_connection": True,
                "user": user,
                "repository": repo,
                "rate_limit": self.github.get_rate_limit().core.remaining
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "github_connection": False,
                "error": str(e)
            }