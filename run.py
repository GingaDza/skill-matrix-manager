#!/usr/bin/env python3
"""アプリケーションのエントリーポイント"""
import sys
import logging
from src.app import App

def setup_logging():
    """ロギングの設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log')
        ]
    )

def main():
    """メインエントリーポイント"""
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("アプリケーションを起動します")
        
        app = App(sys.argv)
        exit_code = app.run()
        
        logger.info("アプリケーションを終了します")
        return exit_code
    except Exception as e:
        logging.getLogger(__name__).exception("予期せぬエラーが発生しました")
        return 1

if __name__ == "__main__":
    sys.exit(main())
