from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from services.recommendation import RecommendationService
import os

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="个性化品味引擎 API",
    description="基于AI的内容推荐系统API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化推荐服务
recommendation_service = RecommendationService()

class RecommendationRequest(BaseModel):
    input: str

@app.get("/")
async def root():
    return {"message": "欢迎使用个性化品味引擎 API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/recommend")
async def get_recommendations(request: RecommendationRequest):
    try:
        recommendations = await recommendation_service.get_recommendations(request.input)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 