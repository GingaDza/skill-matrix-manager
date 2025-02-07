# ... [前のコードと同じ] ...

    def add_user(self):
        """ユーザーの追加"""
        try:
            if self.group_combo.currentIndex() < 0:
                QMessageBox.warning(self, "警告", "グループを選択してください")
                return
                
            name, ok = QInputDialog.getText(self, "ユーザー追加", "ユーザー名を入力:")
            if ok and name:
                group_id = self.group_combo.currentData()
                try:
                    self.db.add_user(name, group_id)
                    self.logger.debug(f"Adding user {name} to group {group_id}")
                    self.load_users(group_id)
                except Exception as e:
                    self.logger.error(f"Database error while adding user: {e}")
                    QMessageBox.critical(self, "エラー", "ユーザーの追加に失敗しました")
        except Exception as e:
            self.logger.error(f"Error in add_user: {e}", exc_info=True)

    def edit_user(self):
        """ユーザーの編集"""
        try:
            selected_items = self.user_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "警告", "ユーザーを選択してください")
                return
                
            current_name = selected_items[0].text()
            new_name, ok = QInputDialog.getText(
                self, "ユーザー編集", 
                "ユーザー名を入力:", 
                text=current_name
            )
            
            if ok and new_name:
                user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
                group_id = self.group_combo.currentData()
                try:
                    if self.db.edit_user(user_id, new_name):
                        self.logger.debug(f"Editing user {user_id} name to {new_name}")
                        self.load_users(group_id)
                    else:
                        raise Exception("User not found")
                except Exception as e:
                    self.logger.error(f"Database error while editing user: {e}")
                    QMessageBox.critical(self, "エラー", "ユーザーの編集に失敗しました")
        except Exception as e:
            self.logger.error(f"Error in edit_user: {e}", exc_info=True)

    def delete_user(self):
        """ユーザーの削除"""
        try:
            selected_items = self.user_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "警告", "ユーザーを選択してください")
                return
                
            reply = QMessageBox.question(
                self, "確認", 
                "選択したユーザーを削除しますか？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
                group_id = self.group_combo.currentData()
                try:
                    if self.db.delete_user(user_id):
                        self.logger.debug(f"Deleting user {user_id}")
                        self.load_users(group_id)
                    else:
                        raise Exception("User not found")
                except Exception as e:
                    self.logger.error(f"Database error while deleting user: {e}")
                    QMessageBox.critical(self, "エラー", "ユーザーの削除に失敗しました")
        except Exception as e:
            self.logger.error(f"Error in delete_user: {e}", exc_info=True)

# ... [残りのコードは同じ] ...
