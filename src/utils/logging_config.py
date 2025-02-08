"""ロギング設定"""
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logging(log_dir: str = "logs", level: str = "INFO"):
    """ロギングを設定
    
    Args:
        log_dir (str): ログファイルを保存するディレクトリ
        level (str): ログレベル（"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"）
    """
    # ログディレクトリを作成
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # ログファイル名を生成（日付を含む）
    log_file = os.path.join(
        log_dir,
        f"skill_matrix_{datetime.now().strftime('%Y%m%d')}.log"
    )
    
    # ロガーの設定
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    # 既存のハンドラをクリア
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # ファイルハンドラーの設定
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    
    # コンソールハンドラーの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # フォーマッターの設定
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # ハンドラーを追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
