from fastapi import FastAPI, Request
from dotenv import load_dotenv
from .services.github_service import GitHubService
from .services.similarity_service import SimilarityService
import os

load_dotenv()

app = FastAPI()
github_service = GitHubService(os.getenv("GITHUB_TOKEN"), os.getenv("GITHUB_REPO"))
similarity_service = SimilarityService()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    
    # Issue作成イベントの場合のみ処理
    if payload.get("action") == "opened" and "issue" in payload:
        issue = payload["issue"]
        issue_number = issue["number"]
        issue_title = issue["title"]
        issue_body = issue["body"] or ""
        
        # 既存のIssueを取得
        existing_issues = github_service.get_open_issues()
        
        # 類似度の計算
        similar_issues = similarity_service.find_similar_issues(
            issue_title, 
            issue_body, 
            existing_issues
        )
        
        if similar_issues:
            # 類似Issueが見つかった場合、コメントを投稿
            comment_body = "似たような Issue が見つかりました：\n\n"
            for sim_issue, similarity in similar_issues:
                comment_body += f"- #{sim_issue.number} ({similarity:.2%} 類似): {sim_issue.title}\n"
            
            github_service.add_comment(issue_number, comment_body)
    
    return {"status": "success"}