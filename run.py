#!/usr/bin/env python3
"""アプリケーション実行スクリプト"""
import sys
import logging
from src.app import App

def main():
    """メイン関数"""
    logger = logging.getLogger(__name__)
    logger.info("アプリケーションを起動します")
    
    try:
        app = App(sys.argv)
        app.run()
    except Exception as e:
        logger.error("予期せぬエラーが発生しました", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
