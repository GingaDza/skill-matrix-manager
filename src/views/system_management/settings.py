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

