import logging
from pathlib import Path
from .database_manager import DatabaseManager

def init_database():
    """データベースの初期化"""
    logger = logging.getLogger(__name__)
    
    try:
        # データベースディレクトリの作成
        db_dir = Path('data')
        db_dir.mkdir(exist_ok=True)
        
        # データベースマネージャーの初期化
        db = DatabaseManager('data/skill_matrix.db')
        db.initialize_database()
        
        # 初期データの投入
        _create_initial_data(db)
        
        logger.info("データベースの初期化が完了しました")
        return True
        
    except Exception as e:
        logger.error(f"データベースの初期化中にエラーが発生: {e}")
        return False

def _create_initial_data(db):
    """初期データの作成"""
    # 開発チームの作成
    db.add_group(
        "開発チーム",
        "システム開発を担当するチーム"
    )
    
    # 基本カテゴリーの作成
    programming_id = db.add_group(
        "プログラミング",
        "プログラミング関連のスキル"
    )
    
    db.add_category(
        "フロントエンド",
        "Webフロントエンド開発",
        programming_id
    )
    
    db.add_category(
        "バックエンド",
        "Webバックエンド開発",
        programming_id
    )
