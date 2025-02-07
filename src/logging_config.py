import logging
from datetime import datetime
import os

def setup_logging():
    # ログディレクトリの作成
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # ログファイル名の設定
    current_time = datetime.now()
    log_file = os.path.join(log_dir, f'app_{current_time.strftime("%Y%m%d_%H%M%S")}.log')

    # ロギングの基本設定
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.debug("Logging system initialized")
    logger.debug(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
