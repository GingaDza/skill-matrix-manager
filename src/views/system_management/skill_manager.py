"""スキル管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit,
    QListWidget, QMessageBox, QInputDialog,
    QSpinBox, QFormLayout
)
from ...database.database_manager import DatabaseManager
import logging

class SkillManager(QWidget):
    """スキル管理クラス"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self._db = db_manager
        self.logger = logging.getLogger(__name__)
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
    
    def _add_skill(self):
        """スキルを追加"""
        name = self.skill_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "警告", "スキル名を入力してください")
            return
            
        parent = self.parent()
        if not parent:
            return
            
        group_name = parent.get_selected_group()
        category_name = parent.get_selected_category()
        
        if not group_name or not category_name:
            QMessageBox.warning(self, "警告", "グループとカテゴリーを選択してください")
            return
            
        try:
            self._db.add_skill(
                name=name,
                description=self.skill_description_input.text().strip(),
                category_name=category_name,
                group_name=group_name,
                min_level=self.min_level_input.value(),
                max_level=self.max_level_input.value()
            )
            self.skill_name_input.clear()
            self.skill_description_input.clear()
            self.min_level_input.setValue(1)
            self.max_level_input.setValue(5)
            self._load_skills(category_name, group_name)
            self.logger.info(
                f"スキルを追加しました: {name} "
                f"(カテゴリー: {category_name}, グループ: {group_name})"
            )
        except Exception as e:
            self.logger.exception("スキルの追加に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"スキルの追加に失敗しました: {str(e)}"
            )
    
    def _load_skills(self, category_name: str, group_name: str):
        """スキル一覧を読み込む"""
        self.skill_list.clear()
        if not category_name or not group_name:
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
    
    def _edit_skill(self):
        """選択されたスキルを編集"""
        current = self.skill_list.currentItem()
        if not current:
            QMessageBox.warning(self, "警告", "編集するスキルを選択してください")
            return
            
        parent = self.parent()
        if not parent:
            return
            
        group_name = parent.get_selected_group()
        category_name = parent.get_selected_category()
        old_name = current.text()
        
        try:
            # 現在のスキル情報を取得
            skill_info = self._db.get_skill(old_name, category_name, group_name)
            
            # 編集ダイアログを表示
            from ..dialogs import EditSkillDialog
            dialog = EditSkillDialog(
                self,
                old_name,
                skill_info['description'],
                skill_info['min_level'],
                skill_info['max_level']
            )
            
            if dialog.exec_():
                new_name = dialog.name
                description = dialog.description
                min_level = dialog.min_level
                max_level = dialog.max_level
                
                self._db.update_skill(
                    old_name=old_name,
                    new_name=new_name,
                    description=description,
                    category_name=category_name,
                    group_name=group_name,
                    min_level=min_level,
                    max_level=max_level
                )
                self._load_skills(category_name, group_name)
                self.logger.info(
                    f"スキルを更新しました: {old_name} -> {new_name} "
                    f"(カテゴリー: {category_name}, グループ: {group_name})"
                )
        except Exception as e:
            self.logger.exception("スキルの更新に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"スキルの更新に失敗しました: {str(e)}"
            )
    
    def _delete_skill(self):
        """選択されたスキルを削除"""
        current = self.skill_list.currentItem()
        if not current:
            QMessageBox.warning(self, "警告", "削除するスキルを選択してください")
            return
            
        parent = self.parent()
        if not parent:
            return
            
        group_name = parent.get_selected_group()
        category_name = parent.get_selected_category()
        name = current.text()
        
        reply = QMessageBox.question(
            self,
            "確認",
            f"スキル「{name}」を削除してもよろしいですか？\n"
            "関連するスキルレベルデータもすべて削除されます。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self._db.delete_skill(
                    name=name,
                    category_name=category_name,
                    group_name=group_name
                )
                self._load_skills(category_name, group_name)
                self.logger.info(
                    f"スキルを削除しました: {name} "
                    f"(カテゴリー: {category_name}, グループ: {group_name})"
                )
            except Exception as e:
                self.logger.exception("スキルの削除に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"スキルの削除に失敗しました: {str(e)}"
                )
