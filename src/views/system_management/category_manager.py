"""カテゴリー管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel,
    QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from ...database.database_manager import DatabaseManager

class CategoryManager(QWidget):
    """カテゴリー管理クラス"""
    
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
        
        # カテゴリー追加部分
        add_layout = QHBoxLayout()
        
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("新しいカテゴリー名")
        add_layout.addWidget(self.category_input)
        
        add_button = QPushButton("追加")
        add_button.clicked.connect(self._add_category)
        add_layout.addWidget(add_button)
        
        layout.addLayout(add_layout)
        
        # カテゴリーリスト
        self.category_list = QListWidget()
        layout.addWidget(self.category_list)
        
        # 削除ボタン
        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self._delete_category)
        layout.addWidget(delete_button)
        
        self.setLayout(layout)
        self._load_categories()
    
    def _load_categories(self):
        """カテゴリー一覧を読み込む"""
        self.category_list.clear()
        if self._db:
            try:
                categories = self._db.get_categories()
                for category in categories:
                    self.category_list.addItem(category)
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"カテゴリーの読み込みに失敗しました: {str(e)}"
                )
    
    def _add_category(self):
        """カテゴリーを追加する"""
        name = self.category_input.text().strip()
        if not name:
            QMessageBox.warning(
                self,
                "警告",
                "カテゴリー名を入力してください"
            )
            return
        
        if self._db:
            try:
                self._db.add_category(name)
                self.category_input.clear()
                self._load_categories()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"カテゴリーの追加に失敗しました: {str(e)}"
                )
    
    def _delete_category(self):
        """選択されたカテゴリーを削除する"""
        current = self.category_list.currentItem()
        if not current:
            QMessageBox.warning(
                self,
                "警告",
                "削除するカテゴリーを選択してください"
            )
            return
        
        if self._db:
            try:
                self._db.delete_category(current.text())
                self._load_categories()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"カテゴリーの削除に失敗しました: {str(e)}"
                )
