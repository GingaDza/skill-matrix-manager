from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QDialogButtonBox
)
from PyQt6.QtCore import Qt

class GroupDialog(QDialog):
    """グループ作成・編集用ダイアログ"""
    
    def __init__(self, parent=None, group_data=None):
        """
        Parameters:
        -----------
        parent : QWidget
            親ウィジェット
        group_data : dict, optional
            編集時の既存グループデータ
            {
                'id': int,
                'name': str,
                'description': str
            }
        """
        super().__init__(parent)
        self.group_data = group_data
        self.setup_ui()
        if group_data:
            self.load_group_data()

    def setup_ui(self):
        """UIコンポーネントの設定"""
        self.setWindowTitle("グループ設定")
        self.setModal(True)
        self.resize(400, 200)

        # メインレイアウト
        layout = QVBoxLayout()
        self.setLayout(layout)

        # グループ名入力
        name_layout = QHBoxLayout()
        name_label = QLabel("グループ名:")
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

        # ボタン
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def load_group_data(self):
        """既存グループデータの読み込み"""
        if self.group_data:
            self.name_edit.setText(self.group_data.get('name', ''))
            self.desc_edit.setText(self.group_data.get('description', ''))

    def get_group_data(self):
        """
        Returns:
        --------
        dict
            入力されたグループデータ
        """
        return {
            'id': self.group_data.get('id') if self.group_data else None,
            'name': self.name_edit.text().strip(),
            'description': self.desc_edit.text().strip()
        }

    def accept(self):
        """OKボタン押下時の処理"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(
                self,
                "入力エラー",
                "グループ名を入力してください。"
            )
            return
        super().accept()
