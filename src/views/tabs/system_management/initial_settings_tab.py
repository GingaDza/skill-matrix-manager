from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QLabel
)
from ....database.database_manager import DatabaseManager

class InitialSettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)

        # グループリスト（左）
        group_widget = QWidget()
        group_layout = QVBoxLayout(group_widget)
        group_layout.addWidget(QLabel("グループリスト"))
        
        self.group_list = QListWidget()
        self.group_list.itemSelectionChanged.connect(self.on_group_selected)
        group_layout.addWidget(self.group_list)

        # グループ操作ボタン
        group_button_layout = QVBoxLayout()
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        
        group_button_layout.addWidget(self.add_group_btn)
        group_button_layout.addWidget(self.edit_group_btn)
        group_button_layout.addWidget(self.delete_group_btn)
        group_layout.addLayout(group_button_layout)

        layout.addWidget(group_widget)

        # カテゴリーリスト（中央）
        category_widget = QWidget()
        category_layout = QVBoxLayout(category_widget)
        category_layout.addWidget(QLabel("親カテゴリーリスト"))
        
        self.category_list = QListWidget()
        self.category_list.itemSelectionChanged.connect(self.on_category_selected)
        category_layout.addWidget(self.category_list)

        # カテゴリー操作ボタン
        category_button_layout = QVBoxLayout()
        self.add_category_btn = QPushButton("追加")
        self.edit_category_btn = QPushButton("編集")
        self.delete_category_btn = QPushButton("削除")
        
        category_button_layout.addWidget(self.add_category_btn)
        category_button_layout.addWidget(self.edit_category_btn)
        category_button_layout.addWidget(self.delete_category_btn)
        category_layout.addLayout(category_button_layout)

        layout.addWidget(category_widget)

        # スキルリスト（右）
        skill_widget = QWidget()
        skill_layout = QVBoxLayout(skill_widget)
        skill_layout.addWidget(QLabel("子カテゴリーリスト"))
        
        self.skill_list = QListWidget()
        self.skill_list.itemSelectionChanged.connect(self.on_skill_selected)
        skill_layout.addWidget(self.skill_list)

        # スキル操作ボタン
        skill_button_layout = QVBoxLayout()
        self.add_skill_btn = QPushButton("追加")
        self.edit_skill_btn = QPushButton("編集")
        self.delete_skill_btn = QPushButton("削除")
        
        skill_button_layout.addWidget(self.add_skill_btn)
        skill_button_layout.addWidget(self.edit_skill_btn)
        skill_button_layout.addWidget(self.delete_skill_btn)
        skill_layout.addLayout(skill_button_layout)

        layout.addWidget(skill_widget)

        # 新規タブ追加ボタン
        tab_button_layout = QVBoxLayout()
        self.add_tab_btn = QPushButton("新規タブ追加")
        self.add_tab_btn.clicked.connect(self.on_add_tab)
        tab_button_layout.addWidget(self.add_tab_btn)
        layout.addLayout(tab_button_layout)

        self.load_initial_data()

    def load_initial_data(self):
        """初期データのロード"""
        # グループリストの更新
        groups = self.db.get_all_groups()
        self.group_list.clear()
        for group in groups:
            self.group_list.addItem(group[1])  # group[1] は name

    def on_group_selected(self):
        """グループ選択時の処理"""
        selected_items = self.group_list.selectedItems()
        if selected_items:
            group_name = selected_items[0].text()
            # グループIDの取得
            groups = self.db.get_all_groups()
            group_id = next((g[0] for g in groups if g[1] == group_name), None)
            if group_id:
                group = self.db.get_group(group_id)
                if group:
                    # カテゴリーリストの更新
                    self.update_category_list(group_id)

    def on_category_selected(self):
        """親カテゴリー選択時の処理"""
        selected_items = self.category_list.selectedItems()
        if selected_items:
            category_name = selected_items[0].text()
            # スキルリストの更新
            self.update_skill_list(category_name)

    def on_skill_selected(self):
        """スキル選択時の処理"""
        pass  # 必要に応じて実装

    def on_add_tab(self):
        """新規タブ追加ボタンのクリックハンドラ"""
        selected_items = self.category_list.selectedItems()
        if selected_items:
            category_name = selected_items[0].text()
            if self.parent() and hasattr(self.parent(), 'add_category_tab'):
                self.parent().add_category_tab(category_name)

    def update_category_list(self, group_id):
        """カテゴリーリストの更新"""
        self.category_list.clear()
        categories = self.db.get_all_categories_with_skills()
        for category in categories:
            self.category_list.addItem(category['category'][1])

    def update_skill_list(self, category_name):
        """スキルリストの更新"""
        self.skill_list.clear()
        categories = self.db.get_all_categories_with_skills()
        for category in categories:
            if category['category'][1] == category_name:
                for skill in category['skills']:
                    self.skill_list.addItem(skill[1])
