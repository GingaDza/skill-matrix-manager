import logging
from datetime import datetime

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # コンソールハンドラ
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # フォーマット
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

# グローバルな現在時刻とユーザー情報
CURRENT_TIME = datetime(2025, 2, 3, 10, 12, 21)
CURRENT_USER = "GingaDza"