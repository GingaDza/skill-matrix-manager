"""スキル管理機能のミックスイン"""
from PyQt6.QtWidgets import QInputDialog, QMessageBox

class SkillManagerMixin:
    """スキル管理機能を提供するミックスイン"""

    def _on_parent_selected(self, row: int):
        """
        親カテゴリー選択時のイベント
        
        Args:
            row (int): 選択された行番号
        """
        try:
            self.logger.info(f"カテゴリー選択: {row}")
            parent_text = self.parent_list.currentItem().text() if self.parent_list.currentItem() else None
            
            if parent_text:
                # スキル一覧を取得
                skills = self._db_manager.get_skills_by_parent(parent_text)
                self.logger.info(f"カテゴリーのスキル: {skills}")
                
                # スキル一覧を更新
                self.child_list.clear()
                self.child_list.addItems(skills)
                
                # ボタンの状態を更新
                self._update_button_states()
                
            else:
                # スキル一覧をクリア
                self.child_list.clear()
                
        except Exception as e:
            self.logger.exception("親カテゴリー選択エラー")

    def _on_add_skill(self):
        """スキル追加"""
        try:
            parent_item = self.parent_list.currentItem()
            if not parent_item:
                raise Exception("カテゴリーを選択してください。")
                
            name, ok = QInputDialog.getText(
                self,
                "スキル追加",
                "スキル名を入力してください:"
            )
            
            if ok and name.strip():
                parent_text = parent_item.text()
                if self._db_manager.add_skill(name.strip(), parent_text):
                    self._on_parent_selected(self.parent_list.currentRow())  # スキル一覧を更新
                    self.logger.info(f"スキル追加: {name} (カテゴリー: {parent_text})")
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
            child_item = self.child_list.currentItem()
            if not child_item:
                raise Exception("編集するスキルを選択してください。")
                
            parent_item = self.parent_list.currentItem()
            if not parent_item:
                raise Exception("カテゴリーを選択してください。")
                
            old_name = child_item.text()
            parent_text = parent_item.text()
            
            new_name, ok = QInputDialog.getText(
                self,
                "スキル編集",
                "新しいスキル名を入力してください:",
                text=old_name
            )
            
            if ok and new_name.strip() and new_name != old_name:
                if self._db_manager.rename_skill(old_name, new_name.strip(), parent_text):
                    self._on_parent_selected(self.parent_list.currentRow())  # スキル一覧を更新
                    self.logger.info(f"スキル名変更: {old_name} → {new_name}")
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
            child_item = self.child_list.currentItem()
            if not child_item:
                raise Exception("削除するスキルを選択してください。")
                
            parent_item = self.parent_list.currentItem()
            if not parent_item:
                raise Exception("カテゴリーを選択してください。")
                
            skill_name = child_item.text()
            parent_text = parent_item.text()
            
            reply = QMessageBox.question(
                self,
                "確認",
                f"スキル「{skill_name}」を削除してもよろしいですか？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if self._db_manager.delete_skill(skill_name, parent_text):
                    self._on_parent_selected(self.parent_list.currentRow())  # スキル一覧を更新
                    self.logger.info(f"スキル削除: {skill_name}")
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