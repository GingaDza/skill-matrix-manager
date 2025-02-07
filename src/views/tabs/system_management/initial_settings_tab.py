from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox
)
from PyQt6.QtCore import Qt
from ...components.lists.group_list_widget import GroupListWidget
from ...components.lists.category_tree_widget import CategoryTreeWidget
from ...dialogs.group_dialog import GroupDialog
from ...dialogs.category_dialog import CategoryDialog
from ...dialogs.skill_dialog import SkillDialog

class InitialSettingsTab(QWidget):
    """システム初期設定タブ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = parent.db if parent else None
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """UIコンポーネントの設定"""
        layout = QHBoxLayout()
        self.setLayout(layout)

        # 左側：グループ管理
        group_container = QWidget()
        group_layout = QVBoxLayout()
        group_container.setLayout(group_layout)

        group_header = QHBoxLayout()
        group_label = QLabel("グループ管理")
        add_group_btn = QPushButton("追加")
        add_group_btn.clicked.connect(self.add_group)
        group_header.addWidget(group_label)
        group_header.addWidget(add_group_btn)
        group_header.addStretch()

        self.group_list = GroupListWidget(self)
        self.group_list.group_selected.connect(self.on_group_selected)

        group_layout.addLayout(group_header)
        group_layout.addWidget(self.group_list)

        # 右側：カテゴリー管理
        category_container = QWidget()
        category_layout = QVBoxLayout()
        category_container.setLayout(category_layout)

        category_header = QHBoxLayout()
        category_label = QLabel("カテゴリー管理")
        add_category_btn = QPushButton("追加")
        add_category_btn.clicked.connect(self.add_category)
        category_header.addWidget(category_label)
        category_header.addWidget(add_category_btn)
        category_header.addStretch()

        self.category_tree = CategoryTreeWidget(self)
        self.category_tree.category_selected.connect(self.on_category_selected)

        category_layout.addLayout(category_header)
        category_layout.addWidget(self.category_tree)

        # レイアウトの追加
        layout.addWidget(group_container)
        layout.addWidget(category_container)

    def load_data(self):
        """データの読み込み"""
        self.group_list.load_groups()
        self.category_tree.load_categories()

    def add_group(self):
        """グループの追加"""
        dialog = GroupDialog(self)
        if dialog.exec():
            group_data = dialog.get_group_data()
            success = self.db.add_group(
                group_data['name'],
                group_data['description']
            )
            if success:
                self.group_list.refresh()
            else:
                QMessageBox.warning(
                    self,
                    "エラー",
                    "グループの追加に失敗しました。"
                )

    def add_category(self):
        """カテゴリーの追加"""
        dialog = CategoryDialog(self)
        if dialog.exec():
            category_data = dialog.get_category_data()
            success = self.db.add_category(
                category_data['name'],
                category_data['description'],
                category_data['parent_id']
            )
            if success:
                self.category_tree.refresh()
            else:
                QMessageBox.warning(
                    self,
                    "エラー",
                    "カテゴリーの追加に失敗しました。"
                )

    def on_group_selected(self, group_id):
        """グループ選択時の処理"""
        group = self.db.get_group(group_id)
        if group:
            dialog = GroupDialog(self, group_data={
                'id': group[0],
                'name': group[1],
                'description': group[2]
            })
            if dialog.exec():
                data = dialog.get_group_data()
                success = self.db.update_group(
                    data['id'],
                    data['name'],
                    data['description']
                )
                if success:
                    self.group_list.refresh()
                else:
                    QMessageBox.warning(
                        self,
                        "エラー",
                        "グループの更新に失敗しました。"
                    )

    def on_category_selected(self, category_id):
        """カテゴリー選択時の処理"""
        category = self.db.get_category(category_id)
        if category:
            dialog = CategoryDialog(
                self,
                category_data={
                    'id': category[0],
                    'name': category[1],
                    'description': category[2],
                    'parent_id': category[3]
                },
                categories=self.db.get_all_categories()
            )
            if dialog.exec():
                data = dialog.get_category_data()
                success = self.db.update_category(
                    data['id'],
                    data['name'],
                    data['description'],
                    data['parent_id']
                )
                if success:
                    self.category_tree.refresh()
                else:
                    QMessageBox.warning(
                        self,
                        "エラー",
                        "カテゴリーの更新に失敗しました。"
                    )
