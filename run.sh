#!/bin/bash

# データベースディレクトリの確認
if [ ! -d "data" ]; then
    mkdir -p data
fi

# ログディレクトリの確認
if [ ! -d "logs" ]; then
    mkdir -p logs
fi

# Pythonスクリプトの実行
python3 run.py
