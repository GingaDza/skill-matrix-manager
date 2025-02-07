[前のコードと同じ内容...]

    def _refresh_data(self):
        """データの更新"""
        self.logger.debug("Starting data refresh")
        if self.is_updating:
            self.logger.debug("Update already in progress, skipping")
            return
            
        try:
            self.is_updating = True
            # グループデータの更新
            groups = self.db.get_all_groups()
            self.logger.debug(f"Fetched {len(groups)} groups")
            
            current_index = self.group_combo.currentIndex()
            current_group_id = self.group_combo.itemData(current_index) if current_index >= 0 else None
            
            self.logger.debug(f"Current group ID: {current_group_id}")
            
            self.group_combo.clear()
            for group_id, group_name in groups:
                self.logger.debug(f"Adding group: {group_id} - {group_name}")
                self.group_combo.addItem(group_name, group_id)
                
            # 現在のグループを再選択
            if current_group_id is not None:
                index = self.group_combo.findData(current_group_id)
                if index >= 0:
                    self.group_combo.setCurrentIndex(index)
                    self.logger.debug(f"Restored selection to group ID: {current_group_id}")
            elif self.group_combo.count() > 0:
                self.group_combo.setCurrentIndex(0)
                self.current_group_id = self.group_combo.itemData(0)
                self.logger.debug(f"Set initial group selection to ID: {self.current_group_id}")
                
            # ユーザーリストの更新
            self._refresh_user_list()
            
            self.logger.debug("Data refresh completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error refreshing data: {e}\n{traceback.format_exc()}")
            QMessageBox.critical(self, "エラー", "データの更新に失敗しました")
        finally:
            self.is_updating = False

    def _refresh_user_list(self):
        """ユーザーリストの更新"""
        self.logger.debug("Starting user list refresh")
        try:
            group_id = self.current_group_id
            if group_id is None:
                self.logger.debug("No group selected, clearing user list")
                self.user_list.clear()
                return
                
            self.logger.debug(f"Fetching users for group {group_id}")
            users = self.db.get_users_by_group(group_id)
            
            self.user_list.clear()
            for user_id, user_name in users:
                self.logger.debug(f"Adding user: {user_id} - {user_name}")
                item = QListWidgetItem(user_name)
                item.setData(Qt.ItemDataRole.UserRole, user_id)
                self.user_list.addItem(item)
                
            self.logger.debug(f"Added {len(users)} users to the list")
                
        except Exception as e:
            self.logger.error(f"Error refreshing user list: {e}\n{traceback.format_exc()}")
            raise

[残りのコードは同じ...]
