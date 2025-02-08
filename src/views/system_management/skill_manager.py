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
                        # 引数を2つに修正
                        skills = self._db_manager.get_skills_by_parent(group_id, parent_name)
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
                
                # 引数を3つに修正 (self + 2)
                if self._db_manager.add_skill(name.strip(), category_name):
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

    def _on_edit_skill(self):
        """スキル編集"""
        try:
            current_item = self.child_list.currentItem()
            if not current_item:
                raise Exception("編集するスキルを選択してください。")
                
            old_name = current_item.text()
            new_name, ok = QInputDialog.getText(
                self,
                "スキル編集",
                "新しいスキル名を入力してください:",
                text=old_name
            )
            
            if ok and new_name.strip() and new_name != old_name:
                group_name = self.category_group_combo.currentText()
                category_name = self.parent_list.currentItem().text()
                
                # 引数を2つに修正
                if self._db_manager.rename_skill(old_name, new_name.strip()):
                    self._on_parent_selected(self.parent_list.currentRow())
                    self.logger.info(f"スキル名変更: {old_name} → {new_name} (カテゴリー: {category_name}, グループ: {group_name})")
                    QMessageBox.information(
                        self,
                        "成功",
                        f"スキル名を「{new_name}」に変更しました。"
                    )
                else:
                    raise Exception("スキル名の変更に失敗しました。")
                
        except Exception as e:
            self.logger.exception("スキル編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _on_delete_skill(self):
        """スキル削除"""
        try:
            current_item = self.child_list.currentItem()
            if not current_item:
                raise Exception("削除するスキルを選択してください。")
                
            skill_name = current_item.text()
            reply = QMessageBox.question(
                self,
                "確認",
                f"スキル「{skill_name}」を削除してもよろしいですか？\n"
                "このスキルに関連する全ての評価データも削除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                group_name = self.category_group_combo.currentText()
                category_name = self.parent_list.currentItem().text()
                
                # 引数を2つに修正
                if self._db_manager.delete_skill(skill_name, category_name):
                    self._on_parent_selected(self.parent_list.currentRow())
                    self.logger.info(f"スキル削除: {skill_name} (カテゴリー: {category_name}, グループ: {group_name})")
                    QMessageBox.information(
                        self,
                        "成功",
                        f"スキル「{skill_name}」を削除しました。"
                    )
                else:
                    raise Exception("スキルの削除に失敗しました。")
                
        except Exception as e:
            self.logger.exception("スキル削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )