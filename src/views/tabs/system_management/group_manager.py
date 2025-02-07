from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QLabel,
    QMessageBox
)
from PyQt6.QtCore import Qt
from ....database.database_manager import DatabaseManager
import logging

class GroupManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        
        # グループリストのラベル
        layout.addWidget(QLabel("グループリスト"))
        
        # グループリスト
        self.group_list = QListWidget()
        self.group_list.itemSelectionChanged.connect(self.on_group_selected)
        layout.addWidget(self.group_list)
        
        # ボタン
        button_layout = QVBoxLayout()
        
        self.add_btn = QPushButton("追加")
        self.edit_btn = QPushButton("編集")
        self.delete_btn = QPushButton("削除")
        
        self.add_btn.clicked.connect(self.add_group)
        self.edit_btn.clicked.connect(self.edit_group)
        self.delete_btn.clicked.connect(self.delete_group)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)

    def load_groups(self):
        """グループリストの読み込み"""
        try:
            self.group_list.clear()
            groups = self.db.get_all_groups()
            
            for group in groups:
                group_id, name = group  # groupは(id, name)のタプル
                item = QListWidgetItem(name)
                item.setData(Qt.ItemDataRole.UserRole, group_id)
                self.group_list.addItem(item)
                
        except Exception as e:
            self.logger.error(f"Error loading groups: {str(e)}")
            raise

    def on_group_selected(self):
        """グループ選択時の処理"""
        selected_items = self.group_list.selectedItems()
        if selected_items:
            group_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
            # グループ選択時の処理を実装

    def add_group(self):
        """グループの追加"""
        # グループ追加の処理を実装
        pass

    def edit_group(self):
        """グループの編集"""
        # グループ編集の処理を実装
        pass

    def delete_group(self):
        """グループの削除"""
        # グループ削除の処理を実装
        pass
