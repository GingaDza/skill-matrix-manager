"""スキル管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit,
    QListWidget, QMessageBox, QSpinBox,
    QFormLayout
)
from ...database.database_manager import DatabaseManager
from ..dialogs import EditSkillDialog
import logging

class SkillManager(QWidget):
    """スキル管理クラス"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self._db = db_manager
        self.logger = logging.getLogger(__name__)
        self._current_group = ""
        self._current_category = ""
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # スキル追加フォーム
        form_layout = QFormLayout()
        
        self.skill_name_input = QLineEdit()
        form_layout.addRow("スキル名:", self.skill_name_input)
        
        self.skill_description_input = QLineEdit()
        form_layout.addRow("説明:", self.skill_description_input)
        
        self.min_level_input = QSpinBox()
        self.min_level_input.setRange(1, 5)
        self.min_level_input.setValue(1)
        form_layout.addRow("最小レベル:", self.min_level_input)
        
        self.max_level_input = QSpinBox()
        self.max_level_input.setRange(1, 5)
        self.max_level_input.setValue(5)
        form_layout.addRow("最大レベル:", self.max_level_input)
        
        add_button = QPushButton("追加")
        add_button.clicked.connect(self._add_skill)
        form_layout.addRow("", add_button)
        
        layout.addLayout(form_layout)
        
        # スキル一覧
        self.skill_list = QListWidget()
        layout.addWidget(self.skill_list)
        
        # 操作ボタン
        button_layout = QHBoxLayout()
        
        edit_button = QPushButton("編集")
        edit_button.clicked.connect(self._edit_skill)
        button_layout.addWidget(edit_button)
        
        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self._delete_skill)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def clear_skills(self):
        """スキル一覧をクリア"""
        self.skill_list.clear()
        self._current_group = ""
        self._current_category = ""
    
    def load_skills(self, group_name: str, category_name: str):
        """スキル一覧を読み込む"""
        self._current_group = group_name
        self._current_category = category_name
        self.skill_list.clear()
        
        try:
            skills = self._db.get_skills(category_name, group_name)
            self.skill_list.addItems([skill['name'] for skill in skills])
        except Exception as e:
            self.logger.exception("スキルの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"スキルの読み込みに失敗しました: {str(e)}"
            )
    
    def _add_skill(self):
        """スキルを追加"""
        if not self._current_group or not self._current_category:
            QMessageBox.warning(self, "警告", "グループとカテゴリーを選択してください")
            return
        
        name = self.skill_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "スキル名を入力してください")
            return
        
        try:
            self._db.add_skill(
                name=name,
                description=self.skill_description_input.text().strip(),
                category_name=self._current_category,
                group_name=self._current_group,
                min_level=self.min_level_input.value(),
                max_level=self.max_level_input.value()
            )
            self.skill_name_input.clear()
            self.skill_description_input.clear()
            self.min_level_input.setValue(1)
            self.max_level_input.setValue(5)
            self.load_skills(self._current_group, self._current_category)
            self.logger.info(
                f"スキルを追加しました: {name} "
                f"(カテゴリー: {self._current_category}, "
                f"グループ: {self._current_group})"
            )
        except Exception as e:
            self.logger.exception("スキルの追加に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"スキルの追加に失敗しました: {str(e)}"
            )

    # ... (残りのメソッドは同様に_current_groupと_current_categoryを使用するように修正)

