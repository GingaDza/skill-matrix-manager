from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem
)
from PyQt6.QtCore import pyqtSignal

class CategoryManagerWidget(QWidget):
    """カテゴリー管理ウィジェット"""

    category_selected = pyqtSignal(int)  # カテゴリー選択時のシグナル

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = parent.db if parent else None
        self.setup_ui()

    def setup_ui(self):
        """UIの設定"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ツールバー
        toolbar = QHBoxLayout()
        
        self.add_button = QPushButton("追加")
        self.add_button.clicked.connect(self.add_category)
        
        self.edit_button = QPushButton("編集")
        self.edit_button.clicked.connect(self.edit_category)
        self.edit_button.setEnabled(False)
        
        self.delete_button = QPushButton("削除")
        self.delete_button.clicked.connect(self.delete_category)
        self.delete_button.setEnabled(False)

        toolbar.addWidget(self.add_button)
        toolbar.addWidget(self.edit_button)
        toolbar.addWidget(self.delete_button)
        toolbar.addStretch()

        # カテゴリーツリー
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["カテゴリー", "説明"])
        self.tree.itemSelectionChanged.connect(self._on_selection_changed)

        layout.addLayout(toolbar)
        layout.addWidget(self.tree)

    def add_category(self):
        """カテゴリーの追加"""
        # TODO: カテゴリー追加ダイアログの表示
        pass

    def edit_category(self):
        """カテゴリーの編集"""
        # TODO: カテゴリー編集ダイアログの表示
        pass

    def delete_category(self):
        """カテゴリーの削除"""
        # TODO: カテゴリー削除の確認と実行
        pass

    def _on_selection_changed(self):
        """選択状態の変更時の処理"""
        selected = self.tree.selectedItems()
        has_selection = len(selected) > 0
        
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        
        if has_selection:
            item = selected[0]
            category_id = item.data(0, Qt.ItemDataRole.UserRole)
            self.category_selected.emit(category_id)
