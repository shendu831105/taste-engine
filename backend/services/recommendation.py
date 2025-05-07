from typing import List, Dict
import openai
from transformers import pipeline
import os
from dotenv import load_dotenv
from .external_api import ExternalAPIService

load_dotenv()

class RecommendationService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.external_api = ExternalAPIService()

    async def get_recommendations(self, user_input: str) -> List[Dict]:
        """
        基于用户输入生成推荐
        """
        try:
            # 使用OpenAI分析用户偏好
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的内容推荐专家。请分析用户的偏好并确定最适合的内容类型（电影、书籍或音乐）。"},
                    {"role": "user", "content": f"分析以下用户偏好，并确定最适合的内容类型：{user_input}"}
                ]
            )
            
            analysis = response.choices[0].message.content
            
            # 根据分析结果选择合适的API调用
            recommendations = []
            if "电影" in analysis.lower():
                movie_recs = await self.external_api.search_movies(user_input)
                recommendations.extend(movie_recs)
            
            if "书" in analysis.lower() or "书籍" in analysis.lower():
                book_recs = await self.external_api.search_books(user_input)
                recommendations.extend(book_recs)
            
            if "音乐" in analysis.lower():
                music_recs = await self.external_api.search_music(user_input)
                recommendations.extend(music_recs)
            
            # 如果没有找到任何推荐，默认搜索所有类型
            if not recommendations:
                movie_recs = await self.external_api.search_movies(user_input)
                book_recs = await self.external_api.search_books(user_input)
                music_recs = await self.external_api.search_music(user_input)
                recommendations = movie_recs + book_recs + music_recs

            # 使用情感分析优化推荐排序
            for rec in recommendations:
                sentiment = self.analyze_sentiment(rec["description"])
                rec["sentiment_score"] = sentiment["score"]
            
            # 根据情感分数排序
            recommendations.sort(key=lambda x: x["sentiment_score"], reverse=True)

            return recommendations[:3]  # 只返回前3个推荐

        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return []

    def analyze_sentiment(self, text: str) -> Dict:
        """
        分析文本情感
        """
        try:
            result = self.sentiment_analyzer(text)[0]
            return {
                "label": result["label"],
                "score": result["score"]
            }
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return {"label": "NEUTRAL", "score": 0.5} 