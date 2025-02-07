from database_manager import DatabaseManager

def initialize_database():
    """データベースを初期化し、テストデータを挿入"""
    db = DatabaseManager()
    
    # テストグループの作成
    group_id = db.add_group("開発チーム", "システム開発チーム")
    
    # テストカテゴリーの作成
    parent_id = db.add_category("プログラミング")
    db.add_category("Python", parent_id)
    db.add_category("JavaScript", parent_id)
    
    parent_id = db.add_category("データベース")
    db.add_category("SQL", parent_id)
    db.add_category("NoSQL", parent_id)

if __name__ == "__main__":
    initialize_database()
