# src/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import api_router
from .database import Base, engine

app = FastAPI(title="Skill Matrix API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの設定
app.include_router(api_router, prefix="/api")  # プレフィックスを "/api" に変更

# 起動時にデータベースのテーブルを作成
Base.metadata.create_all(bind=engine)