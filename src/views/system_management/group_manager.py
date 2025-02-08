"""グループ管理クラスの実装"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget,
    QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from ..dialogs import GroupDialog
from ...database.database_manager import DatabaseManager
import logging

class GroupManager(QWidget):
    """グループ管理クラス"""
    
    # グループ選択/変更シグナル
    group_selected = pyqtSignal(str)
    group_added = pyqtSignal()
    group_deleted = pyqtSignal()
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self._db = db_manager
        self.logger = logging.getLogger(__name__)
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # タイトル
        title = QLabel("グループ管理")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # グループ一覧
        self.group_list = QListWidget()
        self.group_list.currentTextChanged.connect(self._on_group_selected)
        layout.addWidget(self.group_list)
        
        # 操作ボタン
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("追加")
        add_button.clicked.connect(self._add_group)
        button_layout.addWidget(add_button)
        
        edit_button = QPushButton("編集")
        edit_button.clicked.connect(self._edit_group)
        button_layout.addWidget(edit_button)
        
        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self._delete_group)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self._load_groups()
    
    def _load_groups(self):
        """グループ一覧を読み込む"""
        try:
            groups = self._db.get_groups()
            current_text = self.group_list.currentItem()
            current_text = current_text.text() if current_text else ""
            
            self.group_list.clear()
            self.group_list.addItems(groups)
            
            # 既存の選択を維持
            if current_text in groups:
                for i in range(self.group_list.count()):
                    if self.group_list.item(i).text() == current_text:
                        self.group_list.setCurrentRow(i)
                        break
            
        except Exception as e:
            self.logger.exception("グループの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"グループの読み込みに失敗しました: {str(e)}"
            )
    
    def _on_group_selected(self, group_name: str):
        """グループ選択時の処理"""
        self.group_selected.emit(group_name)
    
    def _add_group(self):
        """グループを追加"""
        dialog = GroupDialog(self)
        if dialog.exec_():
            try:
                self._db.add_group(dialog.name)
                self._load_groups()
                self.group_added.emit()
                self.logger.info(f"グループを追加しました: {dialog.name}")
            except Exception as e:
                self.logger.exception("グループの追加に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"グループの追加に失敗しました: {str(e)}"
                )
    
    def _edit_group(self):
        """グループを編集"""
        current_item = self.group_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "編集するグループを選択してください")
            return
            
        old_name = current_item.text()
        dialog = GroupDialog(self, old_name)
        
        if dialog.exec_():
            try:
                self._db.update_group(old_name, dialog.name)
                self._load_groups()
                self.group_added.emit()  # 更新も追加として扱う
                self.logger.info(
                    f"グループを更新しました: {old_name} -> {dialog.name}"
                )
            except Exception as e:
                self.logger.exception("グループの更新に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"グループの更新に失敗しました: {str(e)}"
                )
    
    def _delete_group(self):
        """グループを削除"""
        current_item = self.group_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "削除するグループを選択してください")
            return
            
        name = current_item.text()
        
        reply = QMessageBox.question(
            self,
            "確認",
            f"グループ「{name}」を削除してもよろしいですか？\n"
            "関連するカテゴリー、スキル、ユーザーデータもすべて削除されます。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self._db.delete_group(name)
                self._load_groups()
                self.group_deleted.emit()
                self.logger.info(f"グループを削除しました: {name}")
            except Exception as e:
                self.logger.exception("グループの削除に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"グループの削除に失敗しました: {str(e)}"
                )
    
    def get_selected_group(self) -> str:
        """選択中のグループ名を取得"""
        current_item = self.group_list.currentItem()
        return current_item.text() if current_item else ""
