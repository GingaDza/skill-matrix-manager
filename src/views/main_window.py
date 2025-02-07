# ... [前のコードはそのまま] ...

    def delete_skill(self):
        """スキルの削除"""
        selected_items = self.skill_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '警告', 'スキルを選択してください')
            return

        reply = QMessageBox.question(self, '確認', 
                                   'このスキルを削除してもよろしいですか？',
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            skill_name = selected_items[0].text()
            categories = self.db.get_all_categories_with_skills()
            category_name = self.category_list.selectedItems()[0].text()
            category = next((c for c in categories if c['category'][1] == category_name), None)
            if category:
                skill_id = next((s[0] for s in category['skills'] if s[1] == skill_name), None)
                if skill_id and self.db.delete_category(skill_id):
                    self.load_skills(category_name)
                else:
                    QMessageBox.warning(self, 'エラー', 'スキルの削除に失敗しました')
            else:
                QMessageBox.warning(self, 'エラー', 'スキルの削除に失敗しました')
