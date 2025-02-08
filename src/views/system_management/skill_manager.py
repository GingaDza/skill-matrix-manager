"""スキル管理機能のミックスイン"""
from PyQt6.QtWidgets import QInputDialog, QMessageBox

class SkillManagerMixin:
    """スキル管理機能を提供するミックスイン"""
    
    def _on_parent_selected(self, row: int):
        """親カテゴリー選択時のイベント"""
        try:
            if row >= 0:
                parent_item = self.parent_list.item(row)
                if parent_item:
                    parent_name = parent_item.text()
                    group_name = self.category_group_combo.currentText()
                    self.logger.info(f"選択されたカテゴリー: {parent_name}, グループ: {group_name}")
                    
                    # スキル一覧を取得
                    group_id = self._db_manager.get_group_id_by_name(group_name)
                    if group_id is not None:
                        # メソッド名を修正
                        skills = self._db_manager.get_skills_by_parent(parent_name, group_id)
                        self.logger.info(f"カテゴリーのスキル: {skills}")
                        
                        self.child_list.clear()
                        self.child_list.addItems(skills)
                
        except Exception as e:
            self.logger.exception("親カテゴリー選択エラー")

    def _on_add_skill(self):
        """スキル追加"""
        try:
            parent_item = self.parent_list.currentItem()
            if not parent_item:
                raise Exception("親カテゴリーを選択してください。")
                
            name, ok = QInputDialog.getText(
                self,
                "スキル追加",
                "スキル名を入力してください:"
            )
            
            if ok and name.strip():
                group_name = self.category_group_combo.currentText()
                category_name = parent_item.text()
                
                group_id = self._db_manager.get_group_id_by_name(group_name)
                if group_id is None:
                    raise Exception("グループが見つかりません。")
                
                # 引数の順序を修正
                if self._db_manager.add_skill(name.strip(), group_id, category_name):
                    self._on_parent_selected(self.parent_list.currentRow())
                    self.logger.info(f"スキル追加: {name} (カテゴリー: {category_name}, グループ: {group_name})")
                    QMessageBox.information(
                        self,
                        "成功",
                        f"スキル「{name}」を追加しました。"
                    )
                else:
                    raise Exception("スキルの追加に失敗しました。")
                    
        except Exception as e:
            self.logger.exception("スキル追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )