from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem,
    QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
import logging
from datetime import datetime
from .category_dialog import CategoryDialog

logger = logging.getLogger(__name__)

class CategorySection(QWidget):
    def __init__(self, controllers=None):
        super().__init__()
        self.controllers = controllers
        self.current_time = datetime.now()
        self.current_user = "GingaDza"
        self.setup_ui()
        self.load_categories()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # ツールバー
        toolbar_layout = QHBoxLayout()
        
        # ボタン
        self.add_button = QPushButton("追加")
        self.edit_button = QPushButton("編集")
        self.delete_button = QPushButton("削除")
        
        toolbar_layout.addWidget(self.add_button)
        toolbar_layout.addWidget(self.edit_button)
        toolbar_layout.addWidget(self.delete_button)
        toolbar_layout.addStretch()
        
        # ツリービュー
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabels(["カテゴリ名", "説明"])
        self.category_tree.setColumnWidth(0, 200)
        
        # レイアウトの構築
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.category_tree)

        # イベントの接続
        self.add_button.clicked.connect(self.add_category)
        self.edit_button.clicked.connect(self.edit_category)
        self.delete_button.clicked.connect(self.delete_category)
        self.category_tree.itemSelectionChanged.connect(self.on_selection_changed)
        
        # 初期状態の設定
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def on_selection_changed(self):
        has_selection = len(self.category_tree.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def load_categories(self):
        try:
            from src.services.db import Database
            db = Database.get_instance()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, description, parent_id
                FROM skill_categories
                ORDER BY parent_id NULLS FIRST, name
            """)
            
            categories = cursor.fetchall()
            self.category_tree.clear()
            
            category_items = {}
            
            for category in categories:
                item = QTreeWidgetItem([
                    category[1],
                    category[2] or ""
                ])
                item.setData(0, Qt.ItemDataRole.UserRole, category[0])
                
                if category[3] is None:
                    self.category_tree.addTopLevelItem(item)
                    category_items[category[0]] = item
                else:
                    parent_item = category_items.get(category[3])
                    if parent_item:
                        parent_item.addChild(item)
                    else:
                        self.category_tree.addTopLevelItem(item)
                        
            self.category_tree.expandAll()
            
        except Exception as e:
            logger.error(f"Error loading categories: {e}")
            QMessageBox.critical(self, "エラー", f"カテゴリーの読み込みに失敗しました: {e}")

    def add_category(self):
        dialog = CategoryDialog(self)
        if dialog.exec() == CategoryDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                from src.services.db import Database
                db = Database.get_instance()
                conn = db.get_connection()
                cursor = conn.cursor()
                
                current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                
                cursor.execute("""
                    INSERT INTO skill_categories (
                        name, description, parent_id,
                        created_at, created_by, updated_at, updated_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['name'],
                    data['description'],
                    data['parent_id'],
                    current_time,
                    self.current_user,
                    current_time,
                    self.current_user
                ))
                
                conn.commit()
                self.load_categories()
                
            except Exception as e:
                logger.error(f"Error adding category: {e}")
                QMessageBox.critical(self, "エラー", f"カテゴリーの追加に失敗しました: {e}")

    def edit_category(self):
        selected_item = self.category_tree.currentItem()
        if not selected_item:
            return
            
        category_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
        
        try:
            from src.services.db import Database
            db = Database.get_instance()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, description, parent_id
                FROM skill_categories
                WHERE id = ?
            """, (category_id,))
            
            category = cursor.fetchone()
            if category:
                category_data = {
                    'id': category[0],
                    'name': category[1],
                    'description': category[2],
                    'parent_id': category[3]
                }
                
                dialog = CategoryDialog(self, category_data)
                if dialog.exec() == CategoryDialog.DialogCode.Accepted:
                    data = dialog.get_data()
                    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    
                    cursor.execute("""
                        UPDATE skill_categories
                        SET name = ?, description = ?, parent_id = ?,
                            updated_at = ?, updated_by = ?
                        WHERE id = ?
                    """, (
                        data['name'],
                        data['description'],
                        data['parent_id'],
                        current_time,
                        self.current_user,
                        category_id
                    ))
                    
                    conn.commit()
                    self.load_categories()
                    
        except Exception as e:
            logger.error(f"Error editing category: {e}")
            QMessageBox.critical(self, "エラー", f"カテゴリーの編集に失敗しました: {e}")

    def delete_category(self):
        selected_item = self.category_tree.currentItem()
        if not selected_item:
            return
            
        category_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self,
            '確認',
            'このカテゴリーを削除してもよろしいですか？\n関連する子カテゴリーも削除されます。',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                from src.services.db import Database
                db = Database.get_instance()
                conn = db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM skill_categories
                    WHERE id = ? OR parent_id = ?
                """, (category_id, category_id))
                
                conn.commit()
                self.load_categories()
                
            except Exception as e:
                logger.error(f"Error deleting category: {e}")
                QMessageBox.critical(self, "エラー", f"カテゴリーの削除に失敗しました: {e}")
