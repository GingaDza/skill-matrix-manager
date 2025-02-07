from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QMessageBox,
    QInputDialog
)
from PyQt6.QtCore import Qt
from ..database.database_manager import DatabaseManager
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = DatabaseManager()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("スキルマトリックス管理システム")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # グループパネル
        group_panel = self._create_group_panel()
        layout.addWidget(group_panel)

        # カテゴリーパネル
        category_panel = self._create_category_panel()
        layout.addWidget(category_panel)

        # スキルパネル
        skill_panel = self._create_skill_panel()
        layout.addWidget(skill_panel)

        self.load_groups()

    def _create_group_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("グループリスト"))
        
        self.group_list = QListWidget()
        self.group_list.itemSelectionChanged.connect(self.on_group_selected)
        layout.addWidget(self.group_list)

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        
        self.add_group_btn.clicked.connect(self.add_group)
        self.edit_group_btn.clicked.connect(self.edit_group)
        self.delete_group_btn.clicked.connect(self.delete_group)
        
        button_layout.addWidget(self.add_group_btn)
        button_layout.addWidget(self.edit_group_btn)
        button_layout.addWidget(self.delete_group_btn)
        
        layout.addWidget(button_widget)
        return panel

    def _create_category_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("カテゴリーリスト"))
        
        self.category_list = QListWidget()
        self.category_list.itemSelectionChanged.connect(self.on_category_selected)
        layout.addWidget(self.category_list)

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        self.add_category_btn = QPushButton("追加")
        self.edit_category_btn = QPushButton("編集")
        self.delete_category_btn = QPushButton("削除")
        
        self.add_category_btn.clicked.connect(self.add_category)
        self.edit_category_btn.clicked.connect(self.edit_category)
        self.delete_category_btn.clicked.connect(self.delete_category)
        
        button_layout.addWidget(self.add_category_btn)
        button_layout.addWidget(self.edit_category_btn)
        button_layout.addWidget(self.delete_category_btn)
        
        layout.addWidget(button_widget)
        return panel

    def _create_skill_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.addWidget(QLabel("スキルリスト"))
        
        self.skill_list = QListWidget()
        layout.addWidget(self.skill_list)

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        self.add_skill_btn = QPushButton("追加")
        self.edit_skill_btn = QPushButton("編集")
        self.delete_skill_btn = QPushButton("削除")
        
        self.add_skill_btn.clicked.connect(self.add_skill)
        self.edit_skill_btn.clicked.connect(self.edit_skill)
        self.delete_skill_btn.clicked.connect(self.delete_skill)
        
        button_layout.addWidget(self.add_skill_btn)
        button_layout.addWidget(self.edit_skill_btn)
        button_layout.addWidget(self.delete_skill_btn)
        
        layout.addWidget(button_widget)
        return panel

    def load_groups(self):
        """グループリストの読み込み"""
        self.group_list.clear()
        groups = self.db.get_all_groups()
        for group in groups:
            item = QListWidgetItem(str(group[1]))
            item.setData(Qt.ItemDataRole.UserRole, group[0])  # IDを保存
            self.group_list.addItem(item)

    def on_group_selected(self):
        """グループ選択時の処理"""
        selected = self.group_list.selectedItems()
        if selected:
            group_id = selected[0].data(Qt.ItemDataRole.UserRole)
            self.load_categories(group_id)

    def load_categories(self, group_id):
        """カテゴリーリストの読み込み"""
        self.category_list.clear()
        self.skill_list.clear()
        categories = self.db.get_categories_by_group(group_id)
        for category in categories:
            item = QListWidgetItem(str(category[1]))
            item.setData(Qt.ItemDataRole.UserRole, category[0])  # IDを保存
            self.category_list.addItem(item)

    def on_category_selected(self):
        """カテゴリー選択時の処理"""
        selected = self.category_list.selectedItems()
        if selected:
            category_id = selected[0].data(Qt.ItemDataRole.UserRole)
            self.load_skills(category_id)

    def load_skills(self, category_id):
        """スキルリストの読み込み"""
        self.skill_list.clear()
        skills = self.db.get_skills_by_category(category_id)
        for skill in skills:
            item = QListWidgetItem(str(skill[1]))
            item.setData(Qt.ItemDataRole.UserRole, skill[0])  # IDを保存
            self.skill_list.addItem(item)

    def add_group(self):
        name, ok = QInputDialog.getText(self, 'グループの追加', 'グループ名を入力:')
        if ok and name:
            if self.db.add_group(name):
                self.load_groups()
            else:
                QMessageBox.warning(self, 'エラー', 'グループの追加に失敗しました')

    def edit_group(self):
        if not self.group_list.selectedItems():
            QMessageBox.warning(self, '警告', 'グループを選択してください')
            return
        current = self.group_list.selectedItems()[0]
        name, ok = QInputDialog.getText(self, 'グループの編集', 'グループ名を入力:', 
                                      text=current.text())
        if ok and name:
            group_id = current.data(Qt.ItemDataRole.UserRole)
            if self.db.edit_group(group_id, name):
                self.load_groups()
            else:
                QMessageBox.warning(self, 'エラー', 'グループの編集に失敗しました')

    def delete_group(self):
        if not self.group_list.selectedItems():
            QMessageBox.warning(self, '警告', 'グループを選択してください')
            return
        reply = QMessageBox.question(self, '確認', '削除してよろしいですか？',
                                   QMessageBox.StandardButton.Yes |
                                   QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            current = self.group_list.selectedItems()[0]
            group_id = current.data(Qt.ItemDataRole.UserRole)
            if self.db.delete_group(group_id):
                self.load_groups()
                self.category_list.clear()
                self.skill_list.clear()
            else:
                QMessageBox.warning(self, 'エラー', 'グループの削除に失敗しました')

    def add_category(self):
        if not self.group_list.selectedItems():
            QMessageBox.warning(self, '警告', 'グループを選択してください')
            return
        name, ok = QInputDialog.getText(self, 'カテゴリーの追加', 'カテゴリー名を入力:')
        if ok and name:
            group_id = self.group_list.selectedItems()[0].data(Qt.ItemDataRole.UserRole)
            if self.db.add_category(name, group_id=group_id):
                self.load_categories(group_id)
            else:
                QMessageBox.warning(self, 'エラー', 'カテゴリーの追加に失敗しました')

    def edit_category(self):
        if not self.category_list.selectedItems():
            QMessageBox.warning(self, '警告', 'カテゴリーを選択してください')
            return
        current = self.category_list.selectedItems()[0]
        name, ok = QInputDialog.getText(self, 'カテゴリーの編集', 'カテゴリー名を入力:', 
                                      text=current.text())
        if ok and name:
            category_id = current.data(Qt.ItemDataRole.UserRole)
            if self.db.edit_category(category_id, name):
                group_id = self.group_list.selectedItems()[0].data(Qt.ItemDataRole.UserRole)
                self.load_categories(group_id)
            else:
                QMessageBox.warning(self, 'エラー', 'カテゴリーの編集に失敗しました')

    def delete_category(self):
        if not self.category_list.selectedItems():
            QMessageBox.warning(self, '警告', 'カテゴリーを選択してください')
            return
        reply = QMessageBox.question(self, '確認', '削除してよろしいですか？',
                                   QMessageBox.StandardButton.Yes |
                                   QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            current = self.category_list.selectedItems()[0]
            category_id = current.data(Qt.ItemDataRole.UserRole)
            if self.db.delete_category(category_id):
                group_id = self.group_list.selectedItems()[0].data(Qt.ItemDataRole.UserRole)
                self.load_categories(group_id)
                self.skill_list.clear()
            else:
                QMessageBox.warning(self, 'エラー', 'カテゴリーの削除に失敗しました')

    def add_skill(self):
        if not self.category_list.selectedItems():
            QMessageBox.warning(self, '警告', 'カテゴリーを選択してください')
            return
        name, ok = QInputDialog.getText(self, 'スキルの追加', 'スキル名を入力:')
        if ok and name:
            category_id = self.category_list.selectedItems()[0].data(Qt.ItemDataRole.UserRole)
            group_id = self.group_list.selectedItems()[0].data(Qt.ItemDataRole.UserRole)
            if self.db.add_category(name, parent_id=category_id, group_id=group_id, is_skill=True):
                self.load_skills(category_id)
            else:
                QMessageBox.warning(self, 'エラー', 'スキルの追加に失敗しました')

    def edit_skill(self):
        if not self.skill_list.selectedItems():
            QMessageBox.warning(self, '警告', 'スキルを選択してください')
            return
        current = self.skill_list.selectedItems()[0]
        name, ok = QInputDialog.getText(self, 'スキルの編集', 'スキル名を入力:', 
                                      text=current.text())
        if ok and name:
            skill_id = current.data(Qt.ItemDataRole.UserRole)
            if self.db.edit_category(skill_id, name):
                category_id = self.category_list.selectedItems()[0].data(Qt.ItemDataRole.UserRole)
                self.load_skills(category_id)
            else:
                QMessageBox.warning(self, 'エラー', 'スキルの編集に失敗しました')

    def delete_skill(self):
        if not self.skill_list.selectedItems():
            QMessageBox.warning(self, '警告', 'スキルを選択してください')
            return
        reply = QMessageBox.question(self, '確認', '削除してよろしいですか？',
                                   QMessageBox.StandardButton.Yes |
                                   QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            current = self.skill_list.selectedItems()[0]
            skill_id = current.data(Qt.ItemDataRole.UserRole)
            if self.db.delete_category(skill_id):
                category_id = self.category_list.selectedItems()[0].data(Qt.ItemDataRole.UserRole)
                self.load_skills(category_id)
            else:
                QMessageBox.warning(self, 'エラー', 'スキルの削除に失敗しました')
