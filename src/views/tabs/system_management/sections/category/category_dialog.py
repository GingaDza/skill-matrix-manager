from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QComboBox
)
from PyQt6.QtCore import Qt
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CategoryDialog(QDialog):
    def __init__(self, parent=None, category_data=None):
        super().__init__(parent)
        self.category_data = category_data
        self.setup_ui()
        if category_data:
            self.load_category_data()

    def setup_ui(self):
        self.setWindowTitle("カテゴリー設定")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # カテゴリ名
        name_layout = QHBoxLayout()
        name_label = QLabel("カテゴリ名:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        
        # 説明
        desc_layout = QVBoxLayout()
        desc_label = QLabel("説明:")
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(100)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        
        # 親カテゴリ
        parent_layout = QHBoxLayout()
        parent_label = QLabel("親カテゴリ:")
        self.parent_combo = QComboBox()
        self.parent_combo.addItem("なし", None)
        self.load_parent_categories()
        parent_layout.addWidget(parent_label)
        parent_layout.addWidget(self.parent_combo)
        
        # ボタン
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("キャンセル")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(name_layout)
        layout.addLayout(desc_layout)
        layout.addLayout(parent_layout)
        layout.addLayout(button_layout)
        
        # イベント接続
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

    def load_parent_categories(self):
        try:
            from src.services.db import Database
            db = Database.get_instance()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name FROM skill_categories 
                WHERE parent_id IS NULL 
                ORDER BY name
            """)
            
            categories = cursor.fetchall()
            for category in categories:
                if self.category_data and self.category_data.get('id') != category[0]:
                    self.parent_combo.addItem(category[1], category[0])
                    
        except Exception as e:
            logger.error(f"Error loading parent categories: {e}")

    def load_category_data(self):
        if self.category_data:
            self.name_edit.setText(self.category_data.get('name', ''))
            self.desc_edit.setText(self.category_data.get('description', ''))
            
            parent_id = self.category_data.get('parent_id')
            if parent_id:
                index = self.parent_combo.findData(parent_id)
                if index >= 0:
                    self.parent_combo.setCurrentIndex(index)

    def get_data(self):
        return {
            'name': self.name_edit.text(),
            'description': self.desc_edit.toPlainText(),
            'parent_id': self.parent_combo.currentData()
        }
