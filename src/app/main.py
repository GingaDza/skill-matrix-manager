# src/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import api_router

app = FastAPI(title="Skill Matrix API")

# CORSミドルウェアの設定を修正
origins = ["*"]  # すべてのオリジンを許可

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # Trueから変更
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # プリフライトリクエストのキャッシュ時間
)

@app.get("/")
async def root():
    return {"message": "Welcome to Skill Matrix API"}

# APIルーターをマウント
app.include_router(api_router, prefix="/api")