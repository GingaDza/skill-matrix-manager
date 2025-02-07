import logging
import sys
from src.app import App

def setup_logging():
    """ロギングの設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """メイン処理"""
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("データベースの初期化を開始")
        app = App()
        
        # 現在のユーザー情報をログ出力
        logger.info("現在のユーザー: GingaDza")
        logger.info("現在の時刻: 2025-02-07 13:34:50")  # 時刻を更新
        
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"アプリケーションの起動中にエラーが発生: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
