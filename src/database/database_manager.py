# ... [前のコードはそのまま] ...

    def edit_category(self, category_id, name):
        """カテゴリーを編集"""
        try:
            self.cursor.execute(
                'UPDATE categories SET name = ?, created_at = ?, created_by = ? WHERE id = ?',
                (name, self.current_time, self.current_user, category_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"カテゴリー編集中にエラーが発生: {e}")
            return False

    def delete_category(self, category_id):
        """カテゴリーを削除"""
        try:
            self.cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"カテゴリー削除中にエラーが発生: {e}")
            return False

    def __del__(self):
        """デストラクタ：接続のクローズ"""
        if hasattr(self, 'conn') and self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
