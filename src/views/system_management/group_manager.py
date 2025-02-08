"""グループ管理機能のミックスイン"""
from PyQt6.QtWidgets import QInputDialog, QMessageBox

class GroupManagerMixin:
    """グループ管理機能を提供するミックスイン"""
    
    def _on_group_selected(self, row: int):
        """グループ選択時のイベント"""
        try:
            group_item = self.category_group_combo.itemText(row)
            self.logger.info(f"グループ選択: {group_item}")
            
            # グループ選択を同期
            self._on_category_group_changed(row)
            
            # カテゴリー一覧を取得して最上位を選択
            categories = self._db_manager.get_categories_by_group(group_item)
            if categories:
                self.parent_list.clear()
                self.parent_list.addItems(categories)
                self.parent_list.setCurrentRow(0)  # 最上位のカテゴリーを選択
                self._on_parent_selected(0)  # カテゴリー選択時の処理を実行
                
                # スキル一覧を取得して最上位を選択
                skills = self._db_manager.get_skills_by_parent(categories[0])
                if skills:
                    self.child_list.clear()
                    self.child_list.addItems(skills)
                    self.child_list.setCurrentRow(0)  # 最上位のスキルを選択
            else:
                self.parent_list.clear()
                self.child_list.clear()
                
        except Exception as e:
            self.logger.exception("グループ選択エラー")

    def _on_add_group(self):
        """グループ追加"""
        try:
            name, ok = QInputDialog.getText(
                self,
                "グループ追加",
                "グループ名を入力してください:"
            )
            
            if ok and name.strip():
                if self._db_manager.add_group(name.strip()):
                    self._load_initial_data()
                    self.logger.info(f"グループ追加: {name}")
                    QMessageBox.information(
                        self,
                        "成功",
                        f"グループ「{name}」を追加しました。"
                    )
                else:
                    raise Exception("グループの追加に失敗しました。")
                    
        except Exception as e:
            self.logger.exception("グループ追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _on_edit_group(self):
        """グループ編集"""
        try:
            old_name = self.category_group_combo.currentText()
            if not old_name:
                raise Exception("編集するグループを選択してください。")
                
            new_name, ok = QInputDialog.getText(
                self,
                "グループ編集",
                "新しいグループ名を入力してください:",
                text=old_name
            )
            
            if ok and new_name.strip() and new_name != old_name:
                if self._db_manager.rename_group(old_name, new_name.strip()):
                    self._load_initial_data()
                    self.logger.info(f"グループ名変更: {old_name} → {new_name}")
                    QMessageBox.information(
                        self,
                        "成功",
                        f"グループ名を「{new_name}」に変更しました。"
                    )
                else:
                    raise Exception("グループ名の変更に失敗しました。")
                
        except Exception as e:
            self.logger.exception("グループ編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _on_delete_group(self):
        """グループ削除"""
        try:
            group_name = self.category_group_combo.currentText()
            if not group_name:
                raise Exception("削除するグループを選択してください。")
                
            reply = QMessageBox.question(
                self,
                "確認",
                f"グループ「{group_name}」を削除してもよろしいですか？\n"
                "このグループに属する全てのカテゴリーとスキルも削除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if self._db_manager.delete_group(group_name):
                    self._load_initial_data()
                    self.logger.info(f"グループ削除: {group_name}")
                    QMessageBox.information(
                        self,
                        "成功",
                        f"グループ「{group_name}」を削除しました。"
                    )
                else:
                    raise Exception("グループの削除に失敗しました。")
                
        except Exception as e:
            self.logger.exception("グループ削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _on_category_group_changed(self, row: int):
        """
        グループ選択変更時のイベント
        
        Args:
            row (int): 選択された行番号
        """
        try:
            group_name = self.category_group_combo.currentText()
            self.logger.info(f"グループ選択を同期: {group_name}")
            
            # カテゴリー一覧を更新
            categories = self._db_manager.get_categories_by_group(group_name)
            self.logger.info(f"グループのカテゴリー: {categories}")
            
            self.parent_list.clear()
            self.parent_list.addItems(categories)
            
            # スキル一覧をクリア
            self.child_list.clear()
            
        except Exception as e:
            self.logger.exception("カテゴリーグループ変更エラー")
