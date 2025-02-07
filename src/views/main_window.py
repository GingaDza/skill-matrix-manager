[前のコードの内容を保持...]

    def _connect_signals(self):
        """シグナルの接続"""
        self.logger.debug("Connecting signals")
        try:
            # グループ変更
            self.left_pane.group_changed.connect(self._on_group_changed)
            
            # ユーザー操作
            self.left_pane.add_user_clicked.connect(self.event_handler.add_user)
            self.left_pane.edit_user_clicked.connect(self.event_handler.edit_user)
            self.left_pane.delete_user_clicked.connect(self.event_handler.delete_user)
            
            # データ更新
            self.data_changed.connect(self.data_handler.refresh_data)
            
            # ユーザー削除
            self.user_deleted.connect(self._on_user_deleted)
            
            self.logger.debug("Signal connections completed")
            
        except Exception as e:
            self.logger.error(f"Failed to connect signals: {e}\n{traceback.format_exc()}")

    def _on_group_changed(self, index):
        """グループ変更時の処理"""
        self.logger.debug(f"Group changed to index: {index}")
        try:
            if index >= 0:
                group_id = self.left_pane.group_combo.itemData(index)
                self.data_handler._last_group_id = group_id
                QTimer.singleShot(0, self.data_handler.refresh_user_list)
        except Exception as e:
            self.logger.error(f"Error handling group change: {e}", exc_info=True)

    def _on_user_deleted(self, user_id):
        """ユーザー削除後の処理"""
        self.logger.debug(f"User deleted: {user_id}")
        try:
            self.data_handler.refresh_data()
        except Exception as e:
            self.logger.error(f"Error handling user deletion: {e}", exc_info=True)

[残りのコードは同じ...]
