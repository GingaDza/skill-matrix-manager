#!/usr/bin/env python3
"""アプリケーション起動スクリプト"""
import sys
import logging
import os
from datetime import datetime

def setup_logging():
    """ロギングの設定"""
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                os.path.join(log_dir, 'app.log'),
                encoding='utf-8'
            )
        ]
    )

def main():
    """メイン関数"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        from src.app import App
        
        app = App(sys.argv)
        if app is None:
            logger.error("アプリケーションの初期化に失敗しました")
            return 1
            
        logger.info("アプリケーションを起動します")
        exit_code = app.exec()
        
        logger.info("アプリケーションを終了します")
        return exit_code
        
    except Exception as e:
        logger.exception("予期せぬエラーが発生しました")
        return 1

if __name__ == '__main__':
    sys.exit(main())
