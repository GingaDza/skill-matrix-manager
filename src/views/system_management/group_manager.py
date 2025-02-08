"""グループ管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel,
    QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from ...database.database_manager import DatabaseManager

class GroupManager(QWidget):
    """グループ管理クラス"""
    
    def __init__(self, db_manager: DatabaseManager = None):
        """
        初期化
        
        Args:
            db_manager: データベースマネージャーのインスタンス
        """
        super().__init__()
        self._db = db_manager
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # グループ追加部分
        add_layout = QHBoxLayout()
        
        self.group_input = QLineEdit()
        self.group_input.setPlaceholderText("新しいグループ名")
        add_layout.addWidget(self.group_input)
        
        add_button = QPushButton("追加")
        add_button.clicked.connect(self._add_group)
        add_layout.addWidget(add_button)
        
        layout.addLayout(add_layout)
        
        # グループリスト
        self.group_list = QListWidget()
        layout.addWidget(self.group_list)
        
        # 削除ボタン
        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self._delete_group)
        layout.addWidget(delete_button)
        
        self.setLayout(layout)
        self._load_groups()
    
    def _load_groups(self):
        """グループ一覧を読み込む"""
        self.group_list.clear()
        if self._db:
            try:
                for group in self._db.get_groups():
                    self.group_list.addItem(group)
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"グループの読み込みに失敗しました: {str(e)}"
                )
    
    def _add_group(self):
        """グループを追加する"""
        name = self.group_input.text().strip()
        if not name:
            QMessageBox.warning(
                self,
                "警告",
                "グループ名を入力してください"
            )
            return
        
        if self._db:
            try:
                self._db.add_group(name)
                self.group_input.clear()
                self._load_groups()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"グループの追加に失敗しました: {str(e)}"
                )
    
    def _delete_group(self):
        """選択されたグループを削除する"""
        current = self.group_list.currentItem()
        if not current:
            QMessageBox.warning(
                self,
                "警告",
                "削除するグループを選択してください"
            )
            return
        
        if self._db:
            try:
                self._db.delete_group(current.text())
                self._load_groups()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"グループの削除に失敗しました: {str(e)}"
                )
