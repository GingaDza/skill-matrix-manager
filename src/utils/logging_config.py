"""ロギング設定"""
import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging(log_dir: str = "logs"):
    """ロギングを設定"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # ログファイル名に日付を含める
    log_file = os.path.join(
        log_dir,
        f"skill_matrix_{datetime.now().strftime('%Y%m%d')}.log"
    )
    
    # ロガーの設定
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # ファイルハンドラー
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    
    # コンソールハンドラー
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # フォーマッターの設定
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # ハンドラーの追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
