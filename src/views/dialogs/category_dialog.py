from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
    QDialogButtonBox,
    QTreeWidget,
    QTreeWidgetItem
)
from PyQt6.QtCore import Qt

class CategoryDialog(QDialog):
    """カテゴリー作成・編集用ダイアログ"""
    
    def __init__(self, parent=None, category_data=None, categories=None):
        """
        Parameters:
        -----------
        parent : QWidget
            親ウィジェット
        category_data : dict, optional
            編集時の既存カテゴリーデータ
            {
                'id': int,
                'name': str,
                'description': str,
                'parent_id': int
            }
        categories : list, optional
            既存のカテゴリーリスト
            [{'id': int, 'name': str, 'parent_id': int}, ...]
        """
        super().__init__(parent)
        self.category_data = category_data
        self.categories = categories or []
        self.setup_ui()
        if category_data:
            self.load_category_data()

    def setup_ui(self):
        """UIコンポーネントの設定"""
        self.setWindowTitle("カテゴリー設定")
        self.setModal(True)
        self.resize(500, 300)

        # メインレイアウト
        layout = QVBoxLayout()
        self.setLayout(layout)

        # カテゴリー名入力
        name_layout = QHBoxLayout()
        name_label = QLabel("カテゴリー名:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # 説明入力
        desc_layout = QHBoxLayout()
        desc_label = QLabel("説明:")
        self.desc_edit = QLineEdit()
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_edit)
        layout.addLayout(desc_layout)

        # 親カテゴリー選択
        parent_layout = QHBoxLayout()
        parent_label = QLabel("親カテゴリー:")
        self.parent_combo = QComboBox()
        self.parent_combo.addItem("なし", None)
        for category in self.categories:
            self.parent_combo.addItem(category['name'], category['id'])
        parent_layout.addWidget(parent_label)
        parent_layout.addWidget(self.parent_combo)
        layout.addLayout(parent_layout)

        # ボタン
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def load_category_data(self):
        """既存カテゴリーデータの読み込み"""
        if self.category_data:
            self.name_edit.setText(self.category_data.get('name', ''))
            self.desc_edit.setText(self.category_data.get('description', ''))
            
            # 親カテゴリーの設定
            parent_id = self.category_data.get('parent_id')
            if parent_id is not None:
                index = self.parent_combo.findData(parent_id)
                if index >= 0:
                    self.parent_combo.setCurrentIndex(index)

    def get_category_data(self):
        """
        Returns:
        --------
        dict
            入力されたカテゴリーデータ
        """
        return {
            'id': self.category_data.get('id') if self.category_data else None,
            'name': self.name_edit.text().strip(),
            'description': self.desc_edit.text().strip(),
            'parent_id': self.parent_combo.currentData()
        }

    def accept(self):
        """OKボタン押下時の処理"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(
                self,
                "入力エラー",
                "カテゴリー名を入力してください。"
            )
            return

        # 循環参照チェック
        if self.category_data and self.parent_combo.currentData():
            current_id = self.category_data['id']
            parent_id = self.parent_combo.currentData()
            if self._has_circular_reference(current_id, parent_id):
                QMessageBox.warning(
                    self,
                    "エラー",
                    "循環参照は許可されていません。"
                )
                return
                
        super().accept()

    def _has_circular_reference(self, current_id, parent_id):
        """循環参照のチェック"""
        checked = set()
        while parent_id is not None:
            if parent_id in checked:
                return True
            if parent_id == current_id:
                return True
            checked.add(parent_id)
            # 親カテゴリーを探す
            parent = next(
                (c for c in self.categories if c['id'] == parent_id),
                None
            )
            parent_id = parent['parent_id'] if parent else None
        return False
