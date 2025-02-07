from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QListWidget, QLabel, QMessageBox,
                           QInputDialog)
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
        self.group_list.clear()
        groups = self.db.get_all_groups()
        for group in groups:
            self.group_list.addItem(str(group[1]))

    def on_group_selected(self):
        selected = self.group_list.selectedItems()
        if selected:
            self.load_categories(selected[0].text())

    def load_categories(self, group_name):
        self.category_list.clear()
        self.skill_list.clear()
        categories = self.db.get_all_categories_with_skills()
        for category in categories:
            self.category_list.addItem(category['category'][1])

    def on_category_selected(self):
        selected = self.category_list.selectedItems()
        if selected:
            self.load_skills(selected[0].text())

    def load_skills(self, category_name):
        self.skill_list.clear()
        categories = self.db.get_all_categories_with_skills()
        category = next((c for c in categories if c['category'][1] == category_name), None)
        if category:
            for skill in category['skills']:
                self.skill_list.addItem(skill[1])

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
        current = self.group_list.selectedItems()[0].text()
        name, ok = QInputDialog.getText(self, 'グループの編集', 'グループ名を入力:', text=current)
        if ok and name:
            groups = self.db.get_all_groups()
            group_id = next((g[0] for g in groups if g[1] == current), None)
            if group_id and self.db.edit_group(group_id, name):
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
            current = self.group_list.selectedItems()[0].text()
            groups = self.db.get_all_groups()
            group_id = next((g[0] for g in groups if g[1] == current), None)
            if group_id and self.db.delete_group(group_id):
                self.load_groups()
            else:
                QMessageBox.warning(self, 'エラー', 'グループの削除に失敗しました')

    def add_category(self):
        name, ok = QInputDialog.getText(self, 'カテゴリーの追加', 'カテゴリー名を入力:')
        if ok and name:
            if self.db.add_category(name):
                self.load_categories(self.group_list.selectedItems()[0].text())
            else:
                QMessageBox.warning(self, 'エラー', 'カテゴリーの追加に失敗しました')

    def edit_category(self):
        if not self.category_list.selectedItems():
            QMessageBox.warning(self, '警告', 'カテゴリーを選択してください')
            return
        current = self.category_list.selectedItems()[0].text()
        name, ok = QInputDialog.getText(self, 'カテゴリーの編集', 'カテゴリー名を入力:', text=current)
        if ok and name:
            categories = self.db.get_all_categories_with_skills()
            category_id = next((c['category'][0] for c in categories 
                              if c['category'][1] == current), None)
            if category_id and self.db.edit_category(category_id, name):
                self.load_categories(self.group_list.selectedItems()[0].text())
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
            current = self.category_list.selectedItems()[0].text()
            categories = self.db.get_all_categories_with_skills()
            category_id = next((c['category'][0] for c in categories 
                              if c['category'][1] == current), None)
            if category_id and self.db.delete_category(category_id):
                self.load_categories(self.group_list.selectedItems()[0].text())
            else:
                QMessageBox.warning(self, 'エラー', 'カテゴリーの削除に失敗しました')

    def add_skill(self):
        if not self.category_list.selectedItems():
            QMessageBox.warning(self, '警告', 'カテゴリーを選択してください')
            return
        name, ok = QInputDialog.getText(self, 'スキルの追加', 'スキル名を入力:')
        if ok and name:
            category_name = self.category_list.selectedItems()[0].text()
            categories = self.db.get_all_categories_with_skills()
            parent_id = next((c['category'][0] for c in categories 
                            if c['category'][1] == category_name), None)
            if parent_id and self.db.add_category(name, parent_id, True):
                self.load_skills(category_name)
            else:
                QMessageBox.warning(self, 'エラー', 'スキルの追加に失敗しました')

    def edit_skill(self):
        if not self.skill_list.selectedItems():
            QMessageBox.warning(self, '警告', 'スキルを選択してください')
            return
        current = self.skill_list.selectedItems()[0].text()
        name, ok = QInputDialog.getText(self, 'スキルの編集', 'スキル名を入力:', text=current)
        if ok and name:
            category_name = self.category_list.selectedItems()[0].text()
            categories = self.db.get_all_categories_with_skills()
            category = next((c for c in categories if c['category'][1] == category_name), None)
            if category:
                skill_id = next((s[0] for s in category['skills'] if s[1] == current), None)
                if skill_id and self.db.edit_category(skill_id, name):
                    self.load_skills(category_name)
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
            current = self.skill_list.selectedItems()[0].text()
            category_name = self.category_list.selectedItems()[0].text()
            categories = self.db.get_all_categories_with_skills()
            category = next((c for c in categories if c['category'][1] == category_name), None)
            if category:
                skill_id = next((s[0] for s in category['skills'] if s[1] == current), None)
                if skill_id and self.db.delete_category(skill_id):
                    self.load_skills(category_name)
                else:
                    QMessageBox.warning(self, 'エラー', 'スキルの削除に失敗しました')
