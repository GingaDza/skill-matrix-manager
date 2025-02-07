from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox,
    QPushButton, QMessageBox
)
import logging
from src.desktop.utils.time_utils import TimeProvider

logger = logging.getLogger(__name__)

class SkillDialog(QDialog):
    def __init__(self, category_controller, skill=None, parent=None):
        """
        スキル追加/編集ダイアログ
        
        Args:
            category_controller: カテゴリーコントローラー
            skill: 編集対象のスキル（新規作成時はNone）
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.category_controller = category_controller
        self.skill = skill
        self.skill_data = None
        self.current_time = TimeProvider.get_current_time()
        
        self.init_ui()
        self.load_categories()
        
        if skill:
            self.load_skill_data()
            
    def init_ui(self):
        """UIの初期化"""
        try:
            self.setWindowTitle("スキルの追加" if not self.skill else "スキルの編集")
            
            layout = QVBoxLayout(self)
            layout.setSpacing(10)
            
            # カテゴリー選択
            category_layout = QHBoxLayout()
            category_label = QLabel("カテゴリー:")
            self.category_combo = QComboBox()
            category_layout.addWidget(category_label)
            category_layout.addWidget(self.category_combo)
            layout.addLayout(category_layout)
            
            # スキル名入力
            name_layout = QHBoxLayout()
            name_label = QLabel("スキル名:")
            self.name_edit = QLineEdit()
            self.name_edit.setPlaceholderText("例: Python")
            name_layout.addWidget(name_label)
            name_layout.addWidget(self.name_edit)
            layout.addLayout(name_layout)
            
            # 説明入力
            description_label = QLabel("説明:")
            self.description_edit = QTextEdit()
            self.description_edit.setPlaceholderText("スキルの説明を入力してください")
            self.description_edit.setAcceptRichText(False)
            layout.addWidget(description_label)
            layout.addWidget(self.description_edit)
            
            # ボタン
            button_layout = QHBoxLayout()
            self.ok_button = QPushButton("OK")
            self.cancel_button = QPushButton("キャンセル")
            button_layout.addWidget(self.ok_button)
            button_layout.addWidget(self.cancel_button)
            layout.addLayout(button_layout)
            
            # シグナル/スロット接続
            self.ok_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            
            # ダイアログのサイズ設定
            self.setMinimumWidth(400)
            self.setMinimumHeight(300)
            
            logger.debug(f"{self.current_time} - SkillDialog UI initialized")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to initialize SkillDialog UI: {str(e)}")
            raise
            
    def load_categories(self):
        """カテゴリーの読み込み"""
        try:
            categories = self.category_controller.get_all_categories()
            
            self.category_combo.clear()
            for category in categories:
                self.category_combo.addItem(category.name, category.id)
                
            logger.debug(f"{self.current_time} - Loaded {len(categories)} categories")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to load categories: {str(e)}")
            raise
            
    def load_skill_data(self):
        """編集時のスキルデータを読み込む"""
        try:
            if self.skill:
                # カテゴリーの選択
                index = self.category_combo.findData(self.skill.category_id)
                if index >= 0:
                    self.category_combo.setCurrentIndex(index)
                    
                # スキル名と説明を設定
                self.name_edit.setText(self.skill.name)
                self.description_edit.setText(self.skill.description or "")
                
            logger.debug(f"{self.current_time} - Loaded skill data for editing")
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to load skill data: {str(e)}")
            raise
            
    def accept(self):
        """OKボタンが押された時の処理"""
        try:
            category_id = self.category_combo.currentData()
            name = self.name_edit.text().strip()
            description = self.description_edit.toPlainText().strip()
            
            # 入力値の検証
            if not category_id:
                QMessageBox.warning(self, "警告", "カテゴリーを選択してください。")
                return
                
            if not name:
                QMessageBox.warning(self, "警告", "スキル名を入力してください。")
                return
                
            # スキルデータの設定
            self.skill_data = {
                'category_id': category_id,
                'name': name,
                'description': description if description else None
            }
            
            logger.debug(f"{self.current_time} - Skill data accepted: {name}")
            super().accept()
            
        except Exception as e:
            logger.error(f"{self.current_time} - Failed to process skill data: {str(e)}")
            QMessageBox.critical(self, "エラー", "データの処理に失敗しました。")
            
    def get_skill_data(self) -> dict:
        """入力されたスキルデータを取得"""
        return self.skill_data