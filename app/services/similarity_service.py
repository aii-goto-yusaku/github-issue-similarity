from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import os
import numpy as np

class SimilarityService:
    def __init__(self):
        # 日本語と英語の両方に対応したモデルを使用
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.threshold = float(os.getenv('SIMILARITY_THRESHOLD', 0.8))
    
    def _combine_text(self, title: str, body: str) -> str:
        """タイトルと本文を結合"""
        return f"{title}\n{body}"
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """2つのテキスト間の類似度を計算"""
        embeddings = self.model.encode([text1, text2])
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        return similarity
    
    def find_similar_issues(
        self, 
        current_title: str, 
        current_body: str, 
        existing_issues: List[dict]
    ) -> List[Tuple[dict, float]]:
        """類似するIssueを検索"""
        current_text = self._combine_text(current_title, current_body)
        similar_issues = []
        
        for issue in existing_issues:
            issue_text = self._combine_text(issue['title'], issue['body'])
            similarity = self._calculate_similarity(current_text, issue_text)
            
            if similarity >= self.threshold:
                similar_issues.append((issue, similarity))
        
        # 類似度でソート
        similar_issues.sort(key=lambda x: x[1], reverse=True)
        return similar_issues