from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QMessageBox
)
import logging
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class GroupDialog(QDialog):
    def __init__(self, name: str = "", parent=None):
        """
        グループ追加/編集ダイアログ
        
        Args:
            name: 編集時の初期値（省略時は空文字）
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.name = name
        self.current_time = TimeProvider.get_current_time()
        
        self.init_ui()
        
    def init_ui(self):
        """UIの初期化"""
        try:
            self.setWindowTitle("グループの追加" if not self.name else "グループの編集")
            
            layout = QVBoxLayout(self)
            layout.setSpacing(10)
            
            # グループ名入力
            name_layout = QHBoxLayout()
            name_label = QLabel("グループ名:")
            self.name_edit = QLineEdit(self.name)
            self.name_edit.setPlaceholderText("例: 開発部")
            name_layout.addWidget(name_label)
            name_layout.addWidget(self.name_edit)
            layout.addLayout(name_layout)
            
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
            self.setMinimumWidth(300)
            
            logger.debug(f"{self.current_time} - GroupDialog UI initialized")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to initialize GroupDialog UI: {str(e)}")
            raise
            
    def accept(self):
        """OKボタンが押された時の処理"""
        try:
            name = self.name_edit.text().strip()
            
            if not name:
                QMessageBox.warning(self, "警告", "グループ名を入力してください。")
                return
                
            logger.debug(f"{self.current_time} - Group name accepted: {name}")
            super().accept()
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to process group name: {str(e)}")
            QMessageBox.critical(self, "エラー", "データの処理に失敗しました。")
            
    def get_group_name(self) -> str:
        """入力されたグループ名を取得"""
        return self.name_edit.text().strip()