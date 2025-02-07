    @pyqtSlot(list, list)
    def _handle_update_completed(self, groups: List[Tuple[int, str]], users: List[Tuple[int, str]]):
        """更新完了の処理"""
        try:
            if not self._main_window or not hasattr(self._main_window, 'left_pane'):
                return
                
            left_pane = self._main_window.left_pane
            
            # グループの更新
            with self._handle_ui_update():
                self._update_groups(groups, left_pane)
                if users:
                    self._update_users(users, left_pane)
                left_pane.update_button_states()
                
        except Exception as e:
            self.logger.error(f"更新完了処理エラー: {e}")
        finally:
            self.update_finished.emit()

    @contextmanager
    def _handle_ui_update(self):
        """UI更新のシグナルブロック管理"""
        try:
            left_pane = self._main_window.left_pane
            left_pane.group_combo.blockSignals(True)
            left_pane.user_list.blockSignals(True)
            yield
        finally:
            if hasattr(self, '_main_window') and self._main_window:
                left_pane = self._main_window.left_pane
                left_pane.group_combo.blockSignals(False)
                left_pane.user_list.blockSignals(False)

    def _update_groups(self, groups: List[Tuple[int, str]], left_pane):
        """グループリストの更新"""
        try:
            current_group_id = self._last_group_id
            
            left_pane.group_combo.clear()
            for group_id, group_name in groups:
                left_pane.group_combo.addItem(group_name, group_id)
                
            if current_group_id:
                index = left_pane.group_combo.findData(current_group_id)
                if index >= 0:
                    left_pane.group_combo.setCurrentIndex(index)
                    self._last_group_id = current_group_id
                    
            # キャッシュの更新
            cache_key = f'groups_{datetime.now().timestamp()}'
            self._cache[cache_key] = groups
            self._cache_timestamps[cache_key] = datetime.now()
            
        except Exception as e:
            self.logger.error(f"グループ更新エラー: {e}")

    def _update_users(self, users: List[Tuple[int, str]], left_pane):
        """ユーザーリストの更新"""
        try:
            current_row = left_pane.user_list.currentRow()
            
            left_pane.user_list.clear()
            for user_id, user_name in users:
                item = QListWidgetItem(user_name)
                item.setData(Qt.ItemDataRole.UserRole, user_id)
                left_pane.user_list.addItem(item)
                
            if 0 <= current_row < left_pane.user_list.count():
                left_pane.user_list.setCurrentRow(current_row)
                
            # キャッシュの更新
            if self._last_group_id:
                cache_key = f'users_{self._last_group_id}_{datetime.now().timestamp()}'
                self._cache[cache_key] = users
                self._cache_timestamps[cache_key] = datetime.now()
                
        except Exception as e:
            self.logger.error(f"ユーザーリスト更新エラー: {e}")

    @pyqtSlot(str)
    def _handle_update_error(self, error_msg: str):
        """エラー処理"""
        self.logger.error(f"更新エラー: {error_msg}")
        self._show_error(f"データ更新エラー: {error_msg}")

    def _show_error(self, message: str):
        """エラーメッセージの表示"""
        try:
            QMessageBox.critical(None, "エラー", message)
        except Exception as e:
            self.logger.error(f"エラー表示失敗: {e}")

    def schedule_update(self, immediate: bool = False):
        """更新のスケジュール"""
        try:
            if not immediate and self._is_updating:
                return
                
            interval = 0 if immediate else 250
            self._timers['update'].start(interval)
            
        except Exception as e:
            self.logger.error(f"更新スケジュールエラー: {e}")

    def cleanup(self):
        """終了時のクリーンアップ"""
        try:
            self.logger.info("終了処理開始")
            
            # タイマーの停止
            for timer in self._timers.values():
                timer.stop()
                timer.deleteLater()
            self._timers.clear()
            
            # ワーカーの停止
            for worker in self._workers:
                worker.quit()
                worker.wait()
                worker.deleteLater()
            self._workers.clear()
            
            # キャッシュのクリア
            self._cache.clear()
            self._cache_timestamps.clear()
            
            # 参照のクリア
            self._main_window = None
            self._db = None
            
            # 最終クリーンアップ
            gc.collect()
            
            self.logger.info("終了処理完了")
            
        except Exception as e:
            self.logger.error(f"終了処理エラー: {e}")

    def load_initial_data(self):
        """初期データの読み込み"""
        self.logger.debug("初期データ読み込み開始")
        self.schedule_update(immediate=True)

    def refresh_data(self):
        """データの更新をリクエスト"""
        self.logger.debug("データ更新リクエスト受信")
        self.schedule_update()

    def refresh_user_list(self):
        """ユーザーリストの更新をリクエスト"""
        self.logger.debug("ユーザーリスト更新リクエスト受信")
        if not self._is_updating and self._last_group_id:
            self.schedule_update()
