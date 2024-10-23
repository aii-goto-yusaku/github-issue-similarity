from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from .services.github_service import GitHubService, GitHubConfigError
from .services.similarity_service import SimilarityService
import os
from typing import Dict, Any

load_dotenv()

app = FastAPI(
    title="GitHub Issue Similarity Detector",
    description="A service that detects and recommends similar GitHub issues",
    version="0.1.0",
)

try:
    github_service = GitHubService(os.getenv("GITHUB_TOKEN"), os.getenv("GITHUB_REPO"))
    similarity_service = SimilarityService()
except GitHubConfigError as e:
    # サービス初期化時のエラーを記録
    initialization_error = str(e)
else:
    initialization_error = None

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    システムの健全性をチェックするエンドポイント。
    以下の項目を確認します：
    - GitHubサービスの接続状態
    - 環境変数の設定状態
    - Similarity Serviceの状態
    """
    if initialization_error:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": initialization_error,
                "message": "Service failed to initialize properly"
            }
        )

    health_status = {
        "status": "healthy",
        "version": "0.1.0",
        "services": {
            "similarity_service": {
                "status": "healthy",
                "model": similarity_service.model.get_model_name()
            }
        }
    }

    # GitHub接続状態を確認
    github_status = github_service.check_connection()
    health_status["services"]["github"] = github_status

    # 全体的な健全性を判断
    if not github_status["github_connection"]:
        health_status["status"] = "degraded"
        return JSONResponse(status_code=503, content=health_status)

    return health_status

@app.post("/webhook")
async def github_webhook(request: Request) -> Dict[str, str]:
    """
    GitHubからのWebhookを受け取り、Issue類似度の分析を行うエンドポイント
    """
    # TODO: GitHub Webhook Secretを使用した署名検証機能の実装
    # - X-Hub-Signatureヘッダーの検証を行う
    # - HMAC-SHA256を使用した署名の検証
    # - 不正なリクエストの拒否
    # 参考: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
    if initialization_error:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "message": "Service is not properly initialized",
                "error": initialization_error
            }
        )

    payload = await request.json()
    
    # Issue作成イベントの場合のみ処理
    if payload.get("action") == "opened" and "issue" in payload:
        issue = payload["issue"]
        issue_number = issue["number"]
        issue_title = issue["title"]
        issue_body = issue["body"] or ""
        
        # 既存のIssueを取得（現在作成されたIssueを除く）
        existing_issues = [
            issue for issue in github_service.get_open_issues()
            if issue['number'] != issue_number
        ]
        
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
                comment_body += f"- #{sim_issue['number']} ({similarity:.2%} 類似): {sim_issue['title']}\n"
            
            try:
                github_service.add_comment(issue_number, comment_body)
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={
                        "status": "error",
                        "message": "Failed to add comment",
                        "error": str(e)
                    }
                )
    
    return {"status": "success"}