"""スキル管理クラスの実装"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget,
    QMessageBox, QFormLayout, QLineEdit,
    QSpinBox
)
from PyQt5.QtCore import pyqtSignal, Qt
from ..dialogs import EditSkillDialog
from ...database.database_manager import DatabaseManager
import logging

class SkillManager(QWidget):
    """スキル管理クラス"""
    
    # スキル選択/変更シグナル
    skill_selected = pyqtSignal(str)
    skill_added = pyqtSignal()
    skill_deleted = pyqtSignal()
    
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
        
        # タイトル
        title = QLabel("スキル管理")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
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
        self.skill_list.currentTextChanged.connect(self._on_skill_selected)
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
        self.skill_name_input.clear()
        self.skill_description_input.clear()
        self.min_level_input.setValue(1)
        self.max_level_input.setValue(5)
    
    def load_skills(self, group_name: str, category_name: str):
        """スキル一覧を読み込む"""
        self._current_group = group_name
        self._current_category = category_name
        self.skill_list.clear()
        
        if not group_name or not category_name:
            return
            
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
    
    def _on_skill_selected(self, skill_name: str):
        """スキル選択時の処理"""
        self.skill_selected.emit(skill_name)
    
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
            self.skill_added.emit()
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
    
    def _edit_skill(self):
        """スキルを編集"""
        if not self._current_group or not self._current_category:
            QMessageBox.warning(self, "警告", "グループとカテゴリーを選択してください")
            return
            
        current_item = self.skill_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "編集するスキルを選択してください")
            return
            
        old_name = current_item.text()
        
        try:
            skill = self._db.get_skill(
                old_name,
                self._current_category,
                self._current_group
            )
        except Exception as e:
            self.logger.exception("スキル情報の取得に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"スキル情報の取得に失敗しました: {str(e)}"
            )
            return
            
        dialog = EditSkillDialog(
            self,
            current_name=old_name,
            current_description=skill.get('description', ''),
            current_min_level=skill.get('min_level', 1),
            current_max_level=skill.get('max_level', 5)
        )
        
        if dialog.exec_():
            try:
                self._db.update_skill(
                    old_name=old_name,
                    new_name=dialog.name,
                    description=dialog.description,
                    category_name=self._current_category,
                    group_name=self._current_group,
                    min_level=dialog.min_level,
                    max_level=dialog.max_level
                )
                self.load_skills(self._current_group, self._current_category)
                self.skill_added.emit()  # 更新も追加として扱う
                self.logger.info(
                    f"スキルを更新しました: {old_name} -> {dialog.name} "
                    f"(カテゴリー: {self._current_category}, "
                    f"グループ: {self._current_group})"
                )
            except Exception as e:
                self.logger.exception("スキルの更新に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"スキルの更新に失敗しました: {str(e)}"
                )
    
    def _delete_skill(self):
        """スキルを削除"""
        if not self._current_group or not self._current_category:
            QMessageBox.warning(self, "警告", "グループとカテゴリーを選択してください")
            return
            
        current_item = self.skill_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "削除するスキルを選択してください")
            return
            
        name = current_item.text()
        
        reply = QMessageBox.question(
            self,
            "確認",
            f"スキル「{name}」を削除してもよろしいですか？\n"
            "関連するレベルデータもすべて削除されます。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self._db.delete_skill(
                    name,
                    self._current_category,
                    self._current_group
                )
                self.load_skills(self._current_group, self._current_category)
                self.skill_deleted.emit()
                self.logger.info(
                    f"スキルを削除しました: {name} "
                    f"(カテゴリー: {self._current_category}, "
                    f"グループ: {self._current_group})"
                )
            except Exception as e:
                self.logger.exception("スキルの削除に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"スキルの削除に失敗しました: {str(e)}"
                )

