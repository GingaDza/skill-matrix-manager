#!/bin/bash

# 開発環境のセットアップ確認
echo "開発環境のセットアップを確認中..."
python3 -c "import PyQt6" || {
    echo "PyQt6がインストールされていません。インストールを実行します..."
    pip install PyQt6
}

# テストの実行
echo "テストを実行中..."
PYTHONPATH=. pytest tests/ -v --cov=src

# 終了コードの確認
if [ $? -eq 0 ]; then
    echo "すべてのテストが成功しました。"
else
    echo "テストが失敗しました。"
    exit 1
fi
