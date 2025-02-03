from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
import logging
from datetime import datetime
from src.desktop.utils.time_utils import TimeProvider
from src.desktop.views.dialogs.skill_dialog import SkillDialog

logger = logging.getLogger(__name__)

class SkillManagementWidget(QWidget):
    def __init__(self, category_controller, skill_controller, parent=None):
        super().__init__(parent)
        self.category_controller = category_controller
        self.skill_controller = skill_controller
        self.current_time = datetime(2025, 2, 3, 8, 18, 9)  # TimeProvider.get_current_time()
        
        self.init_ui()
        
    def init_ui(self):
        """UIの初期化"""
        try:
            layout = QVBoxLayout(self)
            
            # ボタンエリア
            button_layout = QHBoxLayout()
            self.add_button = QPushButton("スキル追加")
            self.edit_button = QPushButton("スキル編集")
            self.delete_button = QPushButton("スキル削除")
            
            button_layout.addWidget(self.add_button)
            button_layout.addWidget(self.edit_button)
            button_layout.addWidget(self.delete_button)
            button_layout.addStretch()
            
            layout.addLayout(button_layout)
            
            # スキルテーブル
            self.table = QTableWidget()
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["ID", "スキル名", "説明", "評価済みユーザー数"])
            
            # テーブルのカスタマイズ
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            
            layout.addWidget(self.table)
            
            # シグナル/スロット接続
            self.add_button.clicked.connect(self.on_add_clicked)
            self.edit_button.clicked.connect(self.on_edit_clicked)
            self.delete_button.clicked.connect(self.on_delete_clicked)
            
            logger.debug(f"{self.current_time} - SkillManagementWidget UI initialized")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to initialize SkillManagementWidget UI: {str(e)}")
            raise
            
    def load_skills(self, category_id: int):
        """カテゴリーに属するスキルを読み込む"""
        try:
            skills = self.skill_controller.get_skills_by_category(category_id)
            
            self.table.setRowCount(len(skills))
            for i, skill in enumerate(skills):
                # スキルID
                id_item = QTableWidgetItem(str(skill.id))
                id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, 0, id_item)
                
                # スキル名
                name_item = QTableWidgetItem(skill.name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, 1, name_item)
                
                # 説明
                description_item = QTableWidgetItem(skill.description or "")
                description_item.setFlags(description_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, 2, description_item)
                
                # 評価済みユーザー数（実装予定）
                count_item = QTableWidgetItem("0")
                count_item.setFlags(count_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(i, 3, count_item)
                
            logger.debug(f"{self.current_time} - Loaded {len(skills)} skills for category {category_id}")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to load skills: {str(e)}")
            QMessageBox.critical(self, "エラー", "スキルデータの読み込みに失敗しました。")
            
    def on_add_clicked(self):
        """スキル追加ボタンのクリックハンドラ"""
        try:
            dialog = SkillDialog(self.category_controller, parent=self)
            if dialog.exec() == SkillDialog.DialogCode.Accepted:
                skill_data = dialog.get_skill_data()
                if skill_data:
                    self.skill_controller.create_skill(
                        category_id=skill_data['category_id'],
                        name=skill_data['name'],
                        description=skill_data['description']
                    )
                    self.load_skills(skill_data['category_id'])
                    logger.debug(f"{self.current_time} - Skill added: {skill_data['name']}")
                    QMessageBox.information(self, "成功", "スキルを追加しました。")
                    
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to add skill: {str(e)}")
            QMessageBox.critical(self, "エラー", f"スキルの追加に失敗しました: {str(e)}")
            
    def on_edit_clicked(self):
        """スキル編集ボタンのクリックハンドラ"""
        try:
            current_row = self.table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "警告", "編集するスキルを選択してください。")
                return
                
            skill_id = int(self.table.item(current_row, 0).text())
            skill = self.skill_controller.get_skill(skill_id)
            
            dialog = SkillDialog(self.category_controller, skill=skill, parent=self)
            if dialog.exec() == SkillDialog.DialogCode.Accepted:
                skill_data = dialog.get_skill_data()
                if skill_data:
                    self.skill_controller.update_skill(
                        skill_id,
                        category_id=skill_data['category_id'],
                        name=skill_data['name'],
                        description=skill_data['description']
                    )
                    self.load_skills(skill.category_id)
                    logger.debug(f"{self.current_time} - Skill updated: {skill_data['name']}")
                    QMessageBox.information(self, "成功", "スキルを更新しました。")
                    
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to edit skill: {str(e)}")
            QMessageBox.critical(self, "エラー", f"スキルの編集に失敗しました: {str(e)}")
            
    def on_delete_clicked(self):
        """スキル削除ボタンのクリックハンドラ"""
        try:
            current_row = self.table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "警告", "削除するスキルを選択してください。")
                return
                
            skill_id = int(self.table.item(current_row, 0).text())
            skill = self.skill_controller.get_skill(skill_id)
            skill_name = self.table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self,
                "確認",
                f"スキル「{skill_name}」を削除しますか？\n" +
                "このスキルに対するすべてのユーザー評価も削除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                category_id = skill.category_id
                self.skill_controller.delete_skill(skill_id)
                self.load_skills(category_id)
                logger.debug(f"{self.current_time} - Skill deleted: {skill_name}")
                QMessageBox.information(self, "成功", "スキルを削除しました。")
                
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to delete skill: {str(e)}")
            QMessageBox.critical(self, "エラー", f"スキルの削除に失敗しました: {str(e)}")