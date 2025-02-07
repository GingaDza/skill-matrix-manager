from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QDialogButtonBox
)
from PyQt6.QtCore import Qt

class SkillDialog(QDialog):
    """スキル作成・編集用ダイアログ"""
    
    def __init__(self, parent=None, skill_data=None, categories=None):
        """
        Parameters:
        -----------
        parent : QWidget
            親ウィジェット
        skill_data : dict, optional
            編集時の既存スキルデータ
            {
                'id': int,
                'name': str,
                'description': str,
                'category_id': int,
                'max_level': int
            }
        categories : list, optional
            カテゴリーリスト
            [{'id': int, 'name': str}, ...]
        """
        super().__init__(parent)
        self.skill_data = skill_data
        self.categories = categories or []
        self.setup_ui()
        if skill_data:
            self.load_skill_data()

    def setup_ui(self):
        """UIコンポーネントの設定"""
        self.setWindowTitle("スキル設定")
        self.setModal(True)
        self.resize(500, 400)

        # メインレイアウト
        layout = QVBoxLayout()
        self.setLayout(layout)

        # スキル名入力
        name_layout = QHBoxLayout()
        name_label = QLabel("スキル名:")
        self.name_edit = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # カテゴリー選択
        category_layout = QHBoxLayout()
        category_label = QLabel("カテゴリー:")
        self.category_combo = QComboBox()
        for category in self.categories:
            self.category_combo.addItem(category['name'], category['id'])
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)

        # 最大レベル設定
        level_layout = QHBoxLayout()
        level_label = QLabel("最大レベル:")
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 10)
        self.level_spin.setValue(5)  # デフォルト値
        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_spin)
        layout.addLayout(level_layout)

        # 説明入力
        desc_label = QLabel("説明:")
        self.desc_edit = QTextEdit()
        self.desc_edit.setAcceptRichText(False)
        layout.addWidget(desc_label)
        layout.addWidget(self.desc_edit)

        # レベル説明入力
        self.level_desc_edits = []
        self.level_desc_label = QLabel("レベル別説明:")
        layout.addWidget(self.level_desc_label)
        
        self._update_level_descriptions()
        self.level_spin.valueChanged.connect(self._update_level_descriptions)

        # ボタン
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _update_level_descriptions(self):
        """レベル数に応じて説明入力フィールドを更新"""
        # 既存の説明を保存
        existing_descriptions = {}
        for i, edit in enumerate(self.level_desc_edits):
            if edit.text():
                existing_descriptions[i + 1] = edit.text()

        # 既存のウィジェットをクリア
        for edit in self.level_desc_edits:
            edit.setParent(None)
        self.level_desc_edits.clear()

        # 新しいレベル数で再作成
        max_level = self.level_spin.value()
        for level in range(1, max_level + 1):
            layout = QHBoxLayout()
            label = QLabel(f"レベル{level}:")
            edit = QLineEdit()
            edit.setText(existing_descriptions.get(level, ""))
            layout.addWidget(label)
            layout.addWidget(edit)
            self.layout().insertLayout(self.layout().count() - 1, layout)
            self.level_desc_edits.append(edit)

    def load_skill_data(self):
        """既存スキルデータの読み込み"""
        if self.skill_data:
            self.name_edit.setText(self.skill_data.get('name', ''))
            self.desc_edit.setPlainText(self.skill_data.get('description', ''))
            
            # カテゴリーの設定
            category_id = self.skill_data.get('category_id')
            if category_id is not None:
                index = self.category_combo.findData(category_id)
                if index >= 0:
                    self.category_combo.setCurrentIndex(index)
            
            # 最大レベルの設定
            max_level = self.skill_data.get('max_level', 5)
            self.level_spin.setValue(max_level)
            
            # レベル別説明の設定
            level_descriptions = self.skill_data.get('level_descriptions', {})
            for level, desc in level_descriptions.items():
                if 0 <= level - 1 < len(self.level_desc_edits):
                    self.level_desc_edits[level - 1].setText(desc)

    def get_skill_data(self):
        """
        Returns:
        --------
        dict
            入力されたスキルデータ
        """
        level_descriptions = {}
        for i, edit in enumerate(self.level_desc_edits):
            if edit.text():
                level_descriptions[i + 1] = edit.text()

        return {
            'id': self.skill_data.get('id') if self.skill_data else None,
            'name': self.name_edit.text().strip(),
            'description': self.desc_edit.toPlainText().strip(),
            'category_id': self.category_combo.currentData(),
            'max_level': self.level_spin.value(),
            'level_descriptions': level_descriptions
        }

    def accept(self):
        """OKボタン押下時の処理"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(
                self,
                "入力エラー",
                "スキル名を入力してください。"
            )
            return
        
        if self.category_combo.count() == 0:
            QMessageBox.warning(
                self,
                "エラー",
                "カテゴリーが設定されていません。"
            )
            return

        super().accept()
