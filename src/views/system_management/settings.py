"""初期設定ウィジェット"""
# [前半部分は同じ]

    def load_data(self):
        """データの読み込み"""
        try:
            # グループの読み込み
            groups = self._db_manager.get_groups()
            self.logger.info(f"読み込まれたグループ: {groups}")
            
            # グループリストの更新
            self.group_list.clear()
            self.group_list.addItems(groups)
            
            # グループコンボボックスの更新
            self.category_group_combo.clear()
            self.category_group_combo.addItems(groups)
            
            # 最初のグループのカテゴリーを表示
            if groups:
                self.on_category_group_changed(groups[0])
                
        except Exception as e:
            self.logger.exception("データ読み込みエラー")
            QMessageBox.critical(
                self,
                "エラー",
                "データの読み込みに失敗しました。"
            )

    def on_parent_selected(self, row: int):
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
                        skills = self._db_manager.get_skills_by_category(group_id, parent_name)
                        self.logger.info(f"カテゴリーのスキル: {skills}")
                        
                        self.child_list.clear()
                        self.child_list.addItems(skills)
                
        except Exception as e:
            self.logger.exception("親カテゴリー選択エラー")

    def on_category_group_changed(self, group_name: str):
        """カテゴリー用グループ選択時のイベント"""
        try:
            self.logger.info(f"選択されたグループ: {group_name}")
            
            # グループリストの選択を同期
            items = self.group_list.findItems(group_name, Qt.MatchFlag.MatchExactly)
            if items:
                self.group_list.setCurrentItem(items[0])
            
            # 選択されたグループの親カテゴリーを読み込み
            group_id = self._db_manager.get_group_id_by_name(group_name)
            if group_id is not None:
                categories = self._db_manager.get_parent_categories_by_group(group_id)
                self.logger.info(f"グループのカテゴリー: {categories}")
                
                self.parent_list.clear()
                self.parent_list.addItems(categories)
                self.child_list.clear()
                
                # メインウィンドウのグループ選択も同期
                parent = self.parentWidget()
                while parent:
                    if isinstance(parent, QMainWindow):
                        if hasattr(parent, 'group_combo'):
                            index = parent.group_combo.findText(group_name)
                            if index >= 0:
                                parent.group_combo.setCurrentIndex(index)
                        break
                    parent = parent.parentWidget()
            
        except Exception as e:
            self.logger.exception("カテゴリー読み込みエラー")

    # [その他のメソッドは同じ]

    def on_add_skill(self):
        """スキル追加ボタンのクリックイベント"""
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
                # TODO: スキル追加の実装
                self.on_parent_selected(self.parent_list.currentRow())
                QMessageBox.information(
                    self,
                    "成功",
                    f"スキル「{name}」を追加しました。"
                )
                
        except Exception as e:
            self.logger.exception("スキル追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_edit_skill(self):
        """スキル編集ボタンのクリックイベント"""
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
                # TODO: スキル名の変更処理を実装
                self.on_parent_selected(self.parent_list.currentRow())
                QMessageBox.information(
                    self,
                    "成功",
                    f"スキル名を「{new_name}」に変更しました。"
                )
                
        except Exception as e:
            self.logger.exception("スキル編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_delete_skill(self):
        """スキル削除ボタンのクリックイベント"""
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
                # TODO: スキルの削除処理を実装
                self.on_parent_selected(self.parent_list.currentRow())
                QMessageBox.information(
                    self,
                    "成功",
                    f"スキル「{skill_name}」を削除しました。"
                )
                
        except Exception as e:
            self.logger.exception("スキル削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_add_new_tab(self):
        """新規タブ追加ボタンのクリックイベント"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("タブとして追加する親カテゴリーを選択してください。")
                
            category_name = current_item.text()
            # TODO: メインウィンドウへのタブ追加通知
            QMessageBox.information(
                self,
                "成功",
                f"カテゴリー「{category_name}」をタブとして追加しました。"
            )
            
        except Exception as e:
            self.logger.exception("タブ追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def on_parent_selected(self, row: int):
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
                        skills = self._db_manager.get_skills_by_category(group_id, parent_name)
                        self.logger.info(f"カテゴリーのスキル: {skills}")
                        
                        self.child_list.clear()
                        self.child_list.addItems(skills)
                
        except Exception as e:
            self.logger.exception("親カテゴリー選択エラー")

    def on_category_group_changed(self, group_name: str):
        """カテゴリー用グループ選択時のイベント"""
        try:
            self.logger.info(f"選択されたグループ: {group_name}")
            
            # グループリストの選択を同期
            items = self.group_list.findItems(group_name, Qt.MatchFlag.MatchExactly)
            if items:
                self.group_list.setCurrentItem(items[0])
            
            # 選択されたグループの親カテゴリーを読み込み
            group_id = self._db_manager.get_group_id_by_name(group_name)
            if group_id is not None:
                categories = self._db_manager.get_parent_categories_by_group(group_id)
                self.logger.info(f"グループのカテゴリー: {categories}")
                
                self.parent_list.clear()
                self.parent_list.addItems(categories)
                self.child_list.clear()
                
                # メインウィンドウのグループ選択も同期
                parent = self.parentWidget()
                while parent:
                    if isinstance(parent, QMainWindow):
                        if hasattr(parent, 'group_combo'):
                            index = parent.group_combo.findText(group_name)
                            if index >= 0:
                                parent.group_combo.setCurrentIndex(index)
                        break
                    parent = parent.parentWidget()
            
        except Exception as e:
            self.logger.exception("カテゴリー読み込みエラー")

    def on_group_selected(self, row: int):
        """グループ選択時のイベント"""
        if row >= 0:
            selected_group = self.group_list.item(row).text()
            # コンボボックスの選択を同期
            index = self.category_group_combo.findText(selected_group)
            if index >= 0:
                self.category_group_combo.setCurrentIndex(index)

