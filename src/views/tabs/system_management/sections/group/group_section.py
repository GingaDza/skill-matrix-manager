from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeWidget, QTreeWidgetItem,
    QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
import logging
from .group_dialog import GroupDialog
from src.signals import Signals
from src.config import AppConfig

logger = logging.getLogger(__name__)

class GroupSection(QWidget):
    def __init__(self, controllers=None):
        super().__init__()
        self.controllers = controllers
        self.config = AppConfig.get_instance()
        self.signals = Signals.get_instance()
        self.setup_ui()
        self.load_groups()

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
        
        # グループツリー
        self.group_tree = QTreeWidget()
        self.group_tree.setHeaderLabels(["グループ名", "説明", "メンバー数"])
        self.group_tree.setColumnWidth(0, 150)
        self.group_tree.setColumnWidth(1, 200)
        
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.group_tree)

        # イベントの接続
        self.add_button.clicked.connect(self.add_group)
        self.edit_button.clicked.connect(self.edit_group)
        self.delete_button.clicked.connect(self.delete_group)
        self.group_tree.itemSelectionChanged.connect(self.on_selection_changed)
        
        # 初期状態の設定
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def load_groups(self):
        try:
            from src.services.db import Database
            db = Database.get_instance()
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT d.id, d.name, d.description, COUNT(u.id) as member_count
                FROM departments d
                LEFT JOIN users u ON d.id = u.department_id
                GROUP BY d.id, d.name, d.description
                ORDER BY d.name
            """)
            
            groups = cursor.fetchall()
            self.group_tree.clear()
            
            for group in groups:
                item = QTreeWidgetItem([
                    group[1],
                    group[2] or "",
                    str(group[3])
                ])
                item.setData(0, Qt.ItemDataRole.UserRole, group[0])
                self.group_tree.addTopLevelItem(item)
                
        except Exception as e:
            logger.error(f"Error loading groups: {e}")
            QMessageBox.critical(self, "エラー", f"グループの読み込みに失敗しました: {e}")

    def on_selection_changed(self):
        has_selection = len(self.group_tree.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def add_group(self):
        dialog = GroupDialog(self)
        if dialog.exec() == GroupDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                from src.services.db import Database
                db = Database.get_instance()
                conn = db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO departments (name, description, created_at, created_by, updated_at, updated_by)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    data['name'],
                    data['description'],
                    self.config.current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    self.config.current_user,
                    self.config.current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    self.config.current_user
                ))
                
                conn.commit()
                self.load_groups()
                self.signals.group_changed.emit()
                
            except Exception as e:
                logger.error(f"Error adding group: {e}")
                QMessageBox.critical(self, "エラー", f"グループの追加に失敗しました: {e}")

    def edit_group(self):
        selected_item = self.group_tree.currentItem()
        if not selected_item:
            return
            
        group_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
        group_data = {
            'id': group_id,
            'name': selected_item.text(0),
            'description': selected_item.text(1)
        }
        
        dialog = GroupDialog(self, group_data)
        if dialog.exec() == GroupDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                from src.services.db import Database
                db = Database.get_instance()
                conn = db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE departments
                    SET name = ?, description = ?, updated_at = ?, updated_by = ?
                    WHERE id = ?
                """, (
                    data['name'],
                    data['description'],
                    self.config.current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    self.config.current_user,
                    group_id
                ))
                
                conn.commit()
                self.load_groups()
                self.signals.group_changed.emit()
                
            except Exception as e:
                logger.error(f"Error editing group: {e}")
                QMessageBox.critical(self, "エラー", f"グループの編集に失敗しました: {e}")

    def delete_group(self):
        selected_item = self.group_tree.currentItem()
        if not selected_item:
            return
            
        group_id = selected_item.data(0, Qt.ItemDataRole.UserRole)
        member_count = int(selected_item.text(2))
        
        if member_count > 0:
            QMessageBox.warning(
                self,
                '警告',
                'このグループにはメンバーが存在するため削除できません。\n先にメンバーを別のグループに移動してください。'
            )
            return
            
        reply = QMessageBox.question(
            self,
            '確認',
            'このグループを削除してもよろしいですか？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                from src.services.db import Database
                db = Database.get_instance()
                conn = db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM departments WHERE id = ?", (group_id,))
                conn.commit()
                self.load_groups()
                self.signals.group_changed.emit()
                
            except Exception as e:
                logger.error(f"Error deleting group: {e}")
                QMessageBox.critical(self, "エラー", f"グループの削除に失敗しました: {e}")
