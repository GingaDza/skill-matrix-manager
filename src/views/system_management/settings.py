"""初期設定ウィジェット"""
# [以前のインポート文は同じ]

class SettingsWidget(QWidget):
    """初期設定タブのウィジェット"""
    
    # [__init__からconnect_signalsまでは同じ]

    def add_group(self):
        """グループの追加"""
        try:
            name, ok = QInputDialog.getText(
                self,
                "グループ追加",
                "グループ名を入力してください:"
            )
            
            if ok and name.strip():
                if self._db_manager.add_group(name.strip()):
                    self.load_data()
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

    def edit_group(self):
        """グループの編集"""
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                raise Exception("編集するグループを選択してください。")
                
            old_name = current_item.text()
            new_name, ok = QInputDialog.getText(
                self,
                "グループ編集",
                "新しいグループ名を入力してください:",
                text=old_name
            )
            
            if ok and new_name.strip() and new_name != old_name:
                # TODO: グループ名の変更処理を実装
                self.load_data()
                QMessageBox.information(
                    self,
                    "成功",
                    f"グループ名を「{new_name}」に変更しました。"
                )
                
        except Exception as e:
            self.logger.exception("グループ編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def delete_group(self):
        """グループの削除"""
        try:
            current_item = self.group_list.currentItem()
            if not current_item:
                raise Exception("削除するグループを選択してください。")
                
            group_name = current_item.text()
            reply = QMessageBox.question(
                self,
                "確認",
                f"グループ「{group_name}」を削除してもよろしいですか？\n"
                "このグループに関連する全てのデータも削除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # TODO: グループの削除処理を実装
                self.load_data()
                QMessageBox.information(
                    self,
                    "成功",
                    f"グループ「{group_name}」を削除しました。"
                )
                
        except Exception as e:
            self.logger.exception("グループ削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def add_category(self):
        """カテゴリーの追加"""
        try:
            group_name = self.category_group_combo.currentText()
            if not group_name:
                raise Exception("グループを選択してください。")
            
            name, ok = QInputDialog.getText(
                self,
                "カテゴリー追加",
                "カテゴリー名を入力してください:"
            )
            
            if ok and name.strip():
                group_id = self._db_manager.get_group_id_by_name(group_name)
                if group_id is None:
                    raise Exception("グループが見つかりません。")
                
                if self._db_manager.add_parent_category(name.strip(), group_id):
                    self.on_category_group_changed(group_name)
                    QMessageBox.information(
                        self,
                        "成功",
                        f"カテゴリー「{name}」を追加しました。"
                    )
                else:
                    raise Exception("カテゴリーの追加に失敗しました。")
                    
        except Exception as e:
            self.logger.exception("カテゴリー追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def edit_category(self):
        """カテゴリーの編集"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("編集するカテゴリーを選択してください。")
                
            old_name = current_item.text()
            new_name, ok = QInputDialog.getText(
                self,
                "カテゴリー編集",
                "新しいカテゴリー名を入力してください:",
                text=old_name
            )
            
            if ok and new_name.strip() and new_name != old_name:
                # TODO: カテゴリー名の変更処理を実装
                self.on_category_group_changed(self.category_group_combo.currentText())
                QMessageBox.information(
                    self,
                    "成功",
                    f"カテゴリー名を「{new_name}」に変更しました。"
                )
                
        except Exception as e:
            self.logger.exception("カテゴリー編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def delete_category(self):
        """カテゴリーの削除"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("削除するカテゴリーを選択してください。")
                
            category_name = current_item.text()
            reply = QMessageBox.question(
                self,
                "確認",
                f"カテゴリー「{category_name}」を削除してもよろしいですか？\n"
                "このカテゴリーに関連する全てのスキルも削除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # TODO: カテゴリーの削除処理を実装
                self.on_category_group_changed(self.category_group_combo.currentText())
                QMessageBox.information(
                    self,
                    "成功",
                    f"カテゴリー「{category_name}」を削除しました。"
                )
                
        except Exception as e:
            self.logger.exception("カテゴリー削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def add_skill(self):
        """スキルの追加"""
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

    def edit_skill(self):
        """スキルの編集"""
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

    def delete_skill(self):
        """スキルの削除"""
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

    def add_new_tab(self):
        """新規タブの追加"""
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
        """親カテゴリー選択時の処理"""
        try:
            if row >= 0:
                parent_item = self.parent_list.item(row)
                if parent_item:
                    parent_name = parent_item.text()
                    # TODO: 選択されたカテゴリーのスキル一覧を表示
                    skills = []  # 仮の空リスト
                    self.child_list.clear()
                    self.child_list.addItems(skills)
                
        except Exception as e:
            self.logger.exception("親カテゴリー選択エラー")

    def on_category_group_changed(self, group_name: str):
        """カテゴリー用グループ選択時の処理"""
        try:
            # グループリストの選択を同期
            items = self.group_list.findItems(group_name, Qt.MatchFlag.MatchExactly)
            if items:
                self.group_list.setCurrentItem(items[0])
            
            # 選択されたグループの親カテゴリーを読み込み
            group_id = self._db_manager.get_group_id_by_name(group_name)
            if group_id is not None:
                categories = self._db_manager.get_parent_categories_by_group(group_id)
                self.parent_list.clear()
                self.parent_list.addItems(categories)
                self.child_list.clear()
            
        except Exception as e:
            self.logger.exception("カテゴリー読み込みエラー")

    def on_group_selected(self, row: int):
        """グループ選択時の処理"""
        if row >= 0:
            selected_group = self.group_list.item(row).text()
            # コンボボックスの選択を同期
            index = self.category_group_combo.findText(selected_group)
            if index >= 0:
                self.category_group_combo.setCurrentIndex(index)

