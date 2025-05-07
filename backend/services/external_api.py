import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class ExternalAPIService:
    def __init__(self):
        self.tmdb_api_key = os.getenv("TMDB_API_KEY")
        self.google_books_api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
        self.spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    async def search_movies(self, query: str) -> List[Dict]:
        """
        搜索电影信息
        """
        try:
            response = requests.get(
                "https://api.themoviedb.org/3/search/movie",
                params={
                    "api_key": self.tmdb_api_key,
                    "query": query,
                    "language": "zh-CN"
                }
            )
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "title": movie["title"],
                    "description": movie["overview"],
                    "content_type": "movie"
                }
                for movie in data.get("results", [])[:3]
            ]
        except Exception as e:
            print(f"Error searching movies: {str(e)}")
            return []

    async def search_books(self, query: str) -> List[Dict]:
        """
        搜索图书信息
        """
        try:
            response = requests.get(
                "https://www.googleapis.com/books/v1/volumes",
                params={
                    "q": query,
                    "key": self.google_books_api_key,
                    "langRestrict": "zh",
                    "maxResults": 3
                }
            )
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "title": book["volumeInfo"].get("title", ""),
                    "description": book["volumeInfo"].get("description", ""),
                    "content_type": "book"
                }
                for book in data.get("items", [])
            ]
        except Exception as e:
            print(f"Error searching books: {str(e)}")
            return []

    async def search_music(self, query: str) -> List[Dict]:
        """
        搜索音乐信息
        """
        try:
            # 获取访问令牌
            auth_response = requests.post(
                "https://accounts.spotify.com/api/token",
                {
                    "grant_type": "client_credentials",
                    "client_id": self.spotify_client_id,
                    "client_secret": self.spotify_client_secret,
                }
            )
            auth_response.raise_for_status()
            access_token = auth_response.json()["access_token"]

            # 搜索音乐
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(
                "https://api.spotify.com/v1/search",
                headers=headers,
                params={
                    "q": query,
                    "type": "track",
                    "limit": 3
                }
            )
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "title": track["name"],
                    "description": f"艺术家: {', '.join(artist['name'] for artist in track['artists'])}",
                    "content_type": "music"
                }
                for track in data.get("tracks", {}).get("items", [])
            ]
        except Exception as e:
            print(f"Error searching music: {str(e)}")
            return [] 