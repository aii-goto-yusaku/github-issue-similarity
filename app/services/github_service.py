from github import Github
from typing import List, Tuple

class GitHubService:
    def __init__(self, token: str, repo_name: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)
    
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