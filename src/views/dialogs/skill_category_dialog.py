from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox
)
import logging
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class SkillCategoryDialog(QDialog):
    def __init__(self, name: str = "", description: str = "", parent=None):
        """
        スキルカテゴリー追加/編集ダイアログ
        
        Args:
            name: 編集時の名前の初期値
            description: 編集時の説明の初期値
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.name = name
        self.description = description
        self.category_data = None
        self.current_time = TimeProvider.get_current_time()
        
        self.init_ui()
        
    def init_ui(self):
        """UIの初期化"""
        try:
            self.setWindowTitle("カテゴリーの追加" if not self.name else "カテゴリーの編集")
            
            layout = QVBoxLayout(self)
            layout.setSpacing(10)
            
            # カテゴリー名入力
            name_layout = QHBoxLayout()
            name_label = QLabel("カテゴリー名:")
            self.name_edit = QLineEdit(self.name)
            self.name_edit.setPlaceholderText("例: プログラミング言語")
            name_layout.addWidget(name_label)
            name_layout.addWidget(self.name_edit)
            layout.addLayout(name_layout)
            
            # 説明入力
            description_label = QLabel("説明:")
            self.description_edit = QTextEdit()
            self.description_edit.setPlaceholderText("カテゴリーの説明を入力してください")
            self.description_edit.setText(self.description)
            self.description_edit.setAcceptRichText(False)
            layout.addWidget(description_label)
            layout.addWidget(self.description_edit)
            
            # ボタン
            button_layout = QHBoxLayout()
            self.ok_button = QPushButton("OK")
            self.cancel_button = QPushButton("キャンセル")
            button_layout.addWidget(self.ok_button)
            button_layout.addWidget(self.cancel_button)
            layout.addLayout(button_layout)
            
            # シグナル/スロット接続
            self.ok_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            
            # ダイアログのサイズ設定
            self.setMinimumWidth(400)
            self.setMinimumHeight(300)
            
            logger.debug(f"{self.current_time} - SkillCategoryDialog UI initialized")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to initialize SkillCategoryDialog UI: {str(e)}")
            raise
            
    def accept(self):
        """OKボタンが押された時の処理"""
        try:
            name = self.name_edit.text().strip()
            description = self.description_edit.toPlainText().strip()
            
            if not name:
                QMessageBox.warning(self, "警告", "カテゴリー名を入力してください。")
                return
                
            self.category_data = {
                'name': name,
                'description': description
            }
            
            logger.debug(f"{self.current_time} - Category data accepted: {name}")
            super().accept()
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to process category data: {str(e)}")
            QMessageBox.critical(self, "エラー", "データの処理に失敗しました。")
            
    def get_category_data(self) -> dict:
        """入力されたカテゴリーデータを取得"""
        return self.category_data