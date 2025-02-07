"""データベース管理モジュール"""
# [前の実装の内容を保持...]

    def _create_tables(self):
        """テーブルの作成"""
        cursor = self.conn.cursor()
        
        # グループテーブル
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # 親カテゴリーテーブル（グループとの関連付けを追加）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parent_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                group_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (group_id) REFERENCES groups(id),
                UNIQUE(name, group_id)
            )
        """)
        
        # [その他のテーブル定義は保持...]

    def add_parent_category(self, name: str, group_id: int) -> bool:
        """親カテゴリーの追加"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO parent_categories (name, group_id, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (name, group_id, self.current_time, self.current_time)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.exception(f"親カテゴリー追加エラー: {name}")
            return False

    def get_parent_categories_by_group(self, group_id: int) -> List[str]:
        """グループに属する親カテゴリー一覧の取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT name 
                FROM parent_categories 
                WHERE group_id = ? 
                ORDER BY name
                """,
                (group_id,)
            )
            return [row['name'] for row in cursor.fetchall()]
        except Exception as e:
            self.logger.exception("親カテゴリー一覧取得エラー")
            return []

    def get_group_id_by_name(self, group_name: str) -> Optional[int]:
        """グループ名からIDを取得"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id FROM groups WHERE name = ?",
                (group_name,)
            )
            result = cursor.fetchone()
            return result['id'] if result else None
        except Exception as e:
            self.logger.exception(f"グループID取得エラー: {group_name}")
            return None

