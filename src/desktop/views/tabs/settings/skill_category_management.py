from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt
import logging
from datetime import datetime
from src.desktop.views.dialogs.skill_category_dialog import SkillCategoryDialog
from .skill_management import SkillManagementWidget

logger = logging.getLogger(__name__)

class SkillCategoryManagementWidget(QWidget):
    def __init__(self, category_controller, skill_controller, parent=None):
        super().__init__(parent)
        self.category_controller = category_controller
        self.skill_controller = skill_controller
        self.current_time = datetime(2025, 2, 3, 8, 20, 1)
        self.current_user = "GingaDza"
        
        self.init_ui()
        
    def init_ui(self):
        """UIの初期化"""
        try:
            layout = QVBoxLayout(self)
            
            # 垂直スプリッター
            splitter = QSplitter(Qt.Orientation.Vertical)
            
            # カテゴリー管理部分
            category_widget = QWidget()
            category_layout = QVBoxLayout(category_widget)
            
            # カテゴリーのボタン
            button_layout = QHBoxLayout()
            self.add_button = QPushButton("カテゴリー追加")
            self.edit_button = QPushButton("カテゴリー編集")
            self.delete_button = QPushButton("カテゴリー削除")
            
            button_layout.addWidget(self.add_button)
            button_layout.addWidget(self.edit_button)
            button_layout.addWidget(self.delete_button)
            button_layout.addStretch()
            
            category_layout.addLayout(button_layout)
            
            # カテゴリーテーブル
            self.category_table = QTableWidget()
            self.category_table.setColumnCount(4)
            self.category_table.setHorizontalHeaderLabels(["ID", "カテゴリー名", "説明", "スキル数"])
            
            # テーブルのカスタマイズ
            header = self.category_table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            
            category_layout.addWidget(self.category_table)
            splitter.addWidget(category_widget)
            
            # スキル管理部分
            self.skill_widget = SkillManagementWidget(
                self.category_controller,
                self.skill_controller
            )
            splitter.addWidget(self.skill_widget)
            
            # スプリッターをメインレイアウトに追加
            layout.addWidget(splitter)
            
            # スプリッターの初期サイズ比を設定
            splitter.setSizes([int(self.height() * 0.6), int(self.height() * 0.4)])
            
            # シグナル/スロット接続
            self.add_button.clicked.connect(self.on_add_clicked)
            self.edit_button.clicked.connect(self.on_edit_clicked)
            self.delete_button.clicked.connect(self.on_delete_clicked)
            self.category_table.itemSelectionChanged.connect(self.on_category_selection_changed)
            
            logger.debug(f"{self.current_time} - {self.current_user} initialized SkillCategoryManagementWidget UI")
            
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} failed to initialize SkillCategoryManagementWidget UI: {str(e)}")
            raise
            
    def load_data(self):
        """カテゴリーデータの読み込み"""
        try:
            categories = self.category_controller.get_all_categories()
            
            self.category_table.setRowCount(len(categories))
            for i, category in enumerate(categories):
                # カテゴリーID
                id_item = QTableWidgetItem(str(category.id))
                id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.category_table.setItem(i, 0, id_item)
                
                # カテゴリー名
                name_item = QTableWidgetItem(category.name)
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.category_table.setItem(i, 1, name_item)
                
                # 説明
                description_item = QTableWidgetItem(category.description or "")
                description_item.setFlags(description_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.category_table.setItem(i, 2, description_item)
                
                # スキル数（実装予定）
                count_item = QTableWidgetItem("0")
                count_item.setFlags(count_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.category_table.setItem(i, 3, count_item)
                
            logger.debug(f"{self.current_time} - {self.current_user} loaded {len(categories)} categories")
            
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} failed to load category data: {str(e)}")
            QMessageBox.critical(self, "エラー", "カテゴリーデータの読み込みに失敗しました。")
            
    def on_category_selection_changed(self):
        """カテゴリー選択変更時のハンドラ"""
        try:
            current_row = self.category_table.currentRow()
            if current_row >= 0:
                category_id = int(self.category_table.item(current_row, 0).text())
                self.skill_widget.load_skills(category_id)
            else:
                self.skill_widget.table.setRowCount(0)
                
            logger.debug(f"{self.current_time} - {self.current_user} changed category selection")
            
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} failed to handle category selection: {str(e)}")
            QMessageBox.critical(self, "エラー", "スキルの読み込みに失敗しました。")
            
    def on_add_clicked(self):
        """カテゴリー追加ボタンのクリックハンドラ"""
        try:
            dialog = SkillCategoryDialog(parent=self)
            if dialog.exec() == SkillCategoryDialog.DialogCode.Accepted:
                category_data = dialog.get_category_data()
                if category_data:
                    self.category_controller.create_category(
                        name=category_data['name'],
                        description=category_data['description']
                    )
                    self.load_data()
                    logger.debug(f"{self.current_time} - {self.current_user} added category: {category_data['name']}")
                    QMessageBox.information(self, "成功", "カテゴリーを追加しました。")
                    
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} failed to add category: {str(e)}")
            QMessageBox.critical(self, "エラー", f"カテゴリーの追加に失敗しました: {str(e)}")
            
    def on_edit_clicked(self):
        """カテゴリー編集ボタンのクリックハンドラ"""
        try:
            current_row = self.category_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "警告", "編集するカテゴリーを選択してください。")
                return
                
            category_id = int(self.category_table.item(current_row, 0).text())
            current_name = self.category_table.item(current_row, 1).text()
            current_description = self.category_table.item(current_row, 2).text()
            
            dialog = SkillCategoryDialog(
                name=current_name,
                description=current_description,
                parent=self
            )
            
            if dialog.exec() == SkillCategoryDialog.DialogCode.Accepted:
                category_data = dialog.get_category_data()
                if category_data:
                    self.category_controller.update_category(
                        category_id,
                        name=category_data['name'],
                        description=category_data['description']
                    )
                    self.load_data()
                    logger.debug(f"{self.current_time} - {self.current_user} updated category: {category_data['name']}")
                    QMessageBox.information(self, "成功", "カテゴリーを更新しました。")
                    
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} failed to edit category: {str(e)}")
            QMessageBox.critical(self, "エラー", f"カテゴリーの編集に失敗しました: {str(e)}")
            
    def on_delete_clicked(self):
        """カテゴリー削除ボタンのクリックハンドラ"""
        try:
            current_row = self.category_table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "警告", "削除するカテゴリーを選択してください。")
                return
                
            category_id = int(self.category_table.item(current_row, 0).text())
            category_name = self.category_table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self,
                "確認",
                f"カテゴリー「{category_name}」を削除しますか？\n" +
                "このカテゴリーに属するすべてのスキルも削除されます。",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.category_controller.delete_category(category_id)
                self.load_data()
                self.skill_widget.table.setRowCount(0)  # スキル一覧をクリア
                logger.debug(f"{self.current_time} - {self.current_user} deleted category: {category_name}")
                QMessageBox.information(self, "成功", "カテゴリーを削除しました。")
                
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} failed to delete category: {str(e)}")
            QMessageBox.critical(self, "エラー", f"カテゴリーの削除に失敗しました: {str(e)}")