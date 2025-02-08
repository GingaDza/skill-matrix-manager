"""初期設定ウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QListWidget, QPushButton,
    QInputDialog, QMessageBox, QLabel, QComboBox
)
from PyQt6.QtCore import Qt
from ...database.database_manager import DatabaseManager

class SettingsWidget(QWidget):
    """初期設定タブのウィジェット"""
    
    # [__init__と_init_ui, _create_group_list, _create_category_lists は前回と同じ]

    def _connect_signals(self):
        """シグナルの接続"""
        # グループ操作
        self.add_group_btn.clicked.connect(self._add_group)
        self.edit_group_btn.clicked.connect(self._edit_group)
        self.delete_group_btn.clicked.connect(self._delete_group)
        
        # カテゴリー操作
        self.add_category_btn.clicked.connect(self._add_category)
        self.edit_category_btn.clicked.connect(self._edit_category)
        self.delete_category_btn.clicked.connect(self._delete_category)
        
        # スキル操作
        self.add_skill_btn.clicked.connect(self._add_skill)
        self.edit_skill_btn.clicked.connect(self._edit_skill)
        self.delete_skill_btn.clicked.connect(self._delete_skill)
        
        # タブ操作
        self.new_tab_btn.clicked.connect(self._add_new_tab)
        
        # リスト選択
        self.parent_list.currentRowChanged.connect(self._on_parent_selected)
        self.category_group_combo.currentTextChanged.connect(self._on_category_group_changed)
        self.group_list.currentRowChanged.connect(self._on_group_selected)

    def _add_group(self):
        """グループの追加"""
        try:
            name, ok = QInputDialog.getText(
                self,
                "グループ追加",
                "グループ名を入力してください:"
            )
            
            if ok and name.strip():
                if self._db_manager.add_group(name.strip()):
                    self._load_data()
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

    def _edit_group(self):
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
                self._load_data()
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

    def _delete_group(self):
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
                self._load_data()
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

    def _add_category(self):
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
                    self._on_category_group_changed(group_name)
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

    def _edit_category(self):
        """カテゴリーの編集"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("編集するカテゴリーを選択してください。")
                
            # TODO: カテゴリー編集の実装
            pass
            
        except Exception as e:
            self.logger.exception("カテゴリー編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _delete_category(self):
        """カテゴリーの削除"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("削除するカテゴリーを選択してください。")
                
            # TODO: カテゴリー削除の実装
            pass
            
        except Exception as e:
            self.logger.exception("カテゴリー削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _add_skill(self):
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
                self._on_parent_selected(self.parent_list.currentRow())
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

    def _edit_skill(self):
        """スキルの編集"""
        try:
            current_item = self.child_list.currentItem()
            if not current_item:
                raise Exception("編集するスキルを選択してください。")
                
            # TODO: スキル編集の実装
            pass
            
        except Exception as e:
            self.logger.exception("スキル編集エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _delete_skill(self):
        """スキルの削除"""
        try:
            current_item = self.child_list.currentItem()
            if not current_item:
                raise Exception("削除するスキルを選択してください。")
                
            # TODO: スキル削除の実装
            pass
            
        except Exception as e:
            self.logger.exception("スキル削除エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _add_new_tab(self):
        """新規タブの追加"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("タブとして追加する親カテゴリーを選択してください。")
                
            # TODO: タブ追加の実装
            pass
            
        except Exception as e:
            self.logger.exception("タブ追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )

    def _on_parent_selected(self, row: int):
        """親カテゴリー選択時の処理"""
        try:
            if row >= 0:
                parent_name = self.parent_list.item(row).text()
                # TODO: スキル一覧の表示処理
                pass
                
        except Exception as e:
            self.logger.exception("親カテゴリー選択エラー")

    def _on_category_group_changed(self, group_name: str):
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

    def _on_group_selected(self, row: int):
        """グループ選択時の処理"""
        if row >= 0:
            selected_group = self.group_list.item(row).text()
            # コンボボックスの選択を同期
            index = self.category_group_combo.findText(selected_group)
            if index >= 0:
                self.category_group_combo.setCurrentIndex(index)

