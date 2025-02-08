"""データベース管理クラス"""
# ... (前のコードはそのまま)

    def get_skill(self, name: str, category_name: str, group_name: str) -> Optional[Dict[str, Any]]:
        """スキル情報を取得"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT s.name, s.description, s.min_level, s.max_level
                    FROM skills s
                    JOIN categories c ON s.category_id = c.id
                    JOIN groups g ON c.group_id = g.id
                    WHERE s.name = ? AND c.name = ? AND g.name = ?
                    """,
                    (name, category_name, group_name)
                )
                row = cursor.fetchone()
                return {
                    'name': row[0],
                    'description': row[1],
                    'min_level': row[2],
                    'max_level': row[3]
                } if row else None
        except Exception as e:
            self.logger.exception("スキル情報の取得に失敗しました")
            raise RuntimeError(f"スキル情報の取得に失敗しました: {str(e)}")

    def add_skill(
        self,
        name: str,
        category_name: str,
        group_name: str,
        description: str = "",
        min_level: int = 1,
        max_level: int = 5
    ):
        """スキルを追加"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                
                # カテゴリーIDを取得
                cursor.execute(
                    """
                    SELECT c.id
                    FROM categories c
                    JOIN groups g ON c.group_id = g.id
                    WHERE c.name = ? AND g.name = ?
                    """,
                    (category_name, group_name)
                )
                category_id = cursor.fetchone()
                if not category_id:
                    raise ValueError(f"カテゴリー '{category_name}' またはグループ '{group_name}' が見つかりません")
                
                # スキルを追加
                cursor.execute(
                    """
                    INSERT INTO skills (
                        name, description, category_id,
                        min_level, max_level
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (name, description, category_id[0], min_level, max_level)
                )
                conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"スキル '{name}' は既に存在します")
        except Exception as e:
            self.logger.exception("スキルの追加に失敗しました")
            raise RuntimeError(f"スキルの追加に失敗しました: {str(e)}")
    
    def update_skill(
        self,
        old_name: str,
        new_name: str,
        category_name: str,
        group_name: str,
        description: str = "",
        min_level: int = 1,
        max_level: int = 5
    ):
        """スキルを更新"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()

                # カテゴリーIDを取得
                cursor.execute(
                    """
                    SELECT c.id FROM categories c
                    JOIN groups g ON c.group_id = g.id
                    WHERE c.name = ? AND g.name = ?
                    """,
                    (category_name, group_name)
                )
                category_id = cursor.fetchone()
                if not category_id:
                    raise ValueError(f"カテゴリー '{category_name}' またはグループ '{group_name}' が見つかりません")
                
                # スキルを更新
                cursor.execute(
                    """
                    UPDATE skills
                    SET name = ?, description = ?, min_level = ?, max_level = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE name = ? AND category_id = ?
                    """,
                    (new_name, description, min_level, max_level,
                     old_name, category_id[0])
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"スキル '{old_name}' が見つかりません")
                conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"スキル '{new_name}' は既に存在します")
        except Exception as e:
            self.logger.exception("スキルの更新に失敗しました")
            raise RuntimeError(f"スキルの更新に失敗しました: {str(e)}")

    def delete_skill(self, name: str, category_name: str, group_name: str):
        """スキルを削除"""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()

                # カテゴリーIDを取得
                cursor.execute(
                    """
                    SELECT c.id FROM categories c
                    JOIN groups g ON c.group_id = g.id
                    WHERE c.name = ? AND g.name = ?
                    """,
                    (category_name, group_name)
                )
                category_id = cursor.fetchone()
                if not category_id:
                    raise ValueError(f"カテゴリー '{category_name}' またはグループ '{group_name}' が見つかりません")

                # スキルを削除
                cursor.execute(
                    "DELETE FROM skills WHERE name = ? AND category_id = ?",
                    (name, category_id[0])
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"スキル '{name}' が見つかりません")
                conn.commit()
        except Exception as e:
            self.logger.exception("スキルの削除に失敗しました")
            raise RuntimeError(f"スキルの削除に失敗しました: {str(e)}")
