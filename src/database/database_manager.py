import sqlite3
import logging
from pathlib import Path
import os

class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_path = Path('data/skill_matrix.db')
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 既存のDBファイルを削除して新規作成
        if self.db_path.exists():
            os.remove(self.db_path)
            
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.current_user = "GingaDza"
        self.current_time = "2025-02-07 12:42:54"  # 時刻を更新
        self._initialize_database()

    # ... 他のメソッドは変更なし ...
