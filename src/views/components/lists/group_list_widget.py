from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import pyqtSignal

class GroupListWidget(QListWidget):
    """グループ一覧を表示するウィジェット"""
    
    group_selected = pyqtSignal(int)  # グループ選択時のシグナル

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.db = db if db else parent.db
        self.setup_ui()
        self.load_groups()

    def setup_ui(self):
        """UIの初期設定"""
        self.setAlternatingRowColors(True)
        self.itemClicked.connect(self._on_item_clicked)

    def load_groups(self):
        """グループ一覧の読み込み"""
        self.clear()
        groups = self.db.get_all_groups()
        for group in groups:
            item = QListWidgetItem(group[1])  # group[1] は name
            item.setData(Qt.ItemDataRole.UserRole, group[0])  # group[0] は id
            self.addItem(item)

    def _on_item_clicked(self, item):
        """アイテムクリック時の処理"""
        group_id = item.data(Qt.ItemDataRole.UserRole)
        self.group_selected.emit(group_id)

    def refresh(self):
        """表示の更新"""
        self.load_groups()
