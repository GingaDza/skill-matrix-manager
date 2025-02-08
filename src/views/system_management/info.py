"""システム情報ウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox,
    QLabel, QListWidget, QPushButton,
    QFileDialog
)
from ...database.database_manager import DatabaseManager

class InfoWidget(QWidget):
    """システム情報タブのウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager, parent: QWidget = None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # システム情報
        info_group = QGroupBox("システム情報")
        info_layout = QVBoxLayout()
        
        version_label = QLabel("バージョン: 1.0.0")
        db_label = QLabel("データベース接続: 正常")
        stats_label = QLabel("登録データ数:\nユーザー: 0\nグループ: 0\nスキル: 0")
        
        info_layout.addWidget(version_label)
        info_layout.addWidget(db_label)
        info_layout.addWidget(stats_label)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 操作履歴
        history_group = QGroupBox("操作履歴")
        history_layout = QVBoxLayout()
        
        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        # バックアップ
        backup_group = QGroupBox("バックアップ管理")
        backup_layout = QVBoxLayout()
        
        backup_btn = QPushButton("バックアップを作成")
        restore_btn = QPushButton("バックアップから復元")
        
        backup_layout.addWidget(backup_btn)
        backup_layout.addWidget(restore_btn)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        self.setLayout(layout)
