"""システム管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel,
    QMessageBox, QFrame, QSplitter,
    QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from .group_manager import GroupManager
from .category_manager import CategoryManager
from .skill_manager import SkillManager
from ..data_management import DataManagementWidget
from ..custom_tab import CategoryTab
from ...database.database_manager import DatabaseManager
import logging

class SystemSettingsTab(QWidget):
    """初期設定タブ"""
    
    # グループ変更シグナル
    group_changed = pyqtSignal(str)
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self._db = db_manager
        self.logger = logging.getLogger(__name__)
        self._init_ui()
        
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # グループ選択コンボボックス
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        self.group_combo.currentTextChanged.connect(self._on_group_changed)
        group_layout.addWidget(self.group_combo)
        layout.addLayout(group_layout)
        
        # リストと操作ボタンを配置するスプリッター
        splitter = QSplitter(Qt.Horizontal)
        
        # グループ管理
        self.group_manager = GroupManager(self._db)
        self.group_manager.group_selected.connect(self._update_group_selection)
        self.group_manager.group_added.connect(self._reload_groups)
        self.group_manager.group_deleted.connect(self._reload_groups)
        splitter.addWidget(self.group_manager)
        
        # カテゴリー管理（グループ選択時のみ有効）
        self.category_manager = CategoryManager(self._db)
        self.category_manager.setEnabled(False)
        self.category_manager.category_selected.connect(self._on_category_changed)
        splitter.addWidget(self.category_manager)
        
        # スキル管理用のコンテナ（カテゴリー選択時のみ有効）
        skill_container = QWidget()
        skill_layout = QVBoxLayout(skill_container)
        
        # スキル管理のタイトル
        skill_title = QLabel("スキル管理")
        skill_title.setAlignment(Qt.AlignCenter)
        skill_layout.addWidget(skill_title)
        
        # スキル管理ウィジェット
        self.skill_manager = SkillManager(self._db)
        self.skill_manager.setEnabled(False)
        skill_layout.addWidget(self.skill_manager)
        
        splitter.addWidget(skill_container)
        
        # スプリッターの比率を設定
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 1)
        
        layout.addWidget(splitter)
        
        # 新規タブ追加ボタン（カテゴリー選択時のみ有効）
        add_tab_frame = QFrame()
        add_tab_frame.setFrameStyle(QFrame.StyledPanel)
        add_tab_layout = QHBoxLayout()
        
        self.add_tab_btn = QPushButton("選択したカテゴリーで新規タブを追加")
        self.add_tab_btn.clicked.connect(self._add_custom_tab)
        self.add_tab_btn.setEnabled(False)
        add_tab_layout.addWidget(self.add_tab_btn)
        
        add_tab_frame.setLayout(add_tab_layout)
        layout.addWidget(add_tab_frame)
        
        self.setLayout(layout)
        self._load_groups()
    
    def _load_groups(self):
        """グループ一覧を読み込む"""
        try:
            groups = self._db.get_groups()
            current_text = self.group_combo.currentText()
            
            self.group_combo.clear()
            self.group_combo.addItems(groups)
            
            # 既存の選択を維持
            if current_text in groups:
                self.group_combo.setCurrentText(current_text)
            
        except Exception as e:
            self.logger.exception("グループの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"グループの読み込みに失敗しました: {str(e)}"
            )
    
    def _reload_groups(self):
        """グループ一覧を再読み込み"""
        self._load_groups()
        self.group_changed.emit(self.group_combo.currentText())
    
    def _update_group_selection(self, group_name: str):
        """グループ選択を更新"""
        if group_name != self.group_combo.currentText():
            self.group_combo.setCurrentText(group_name)
    
    def _on_group_changed(self, group_name: str):
        """グループ変更時の処理"""
        self.category_manager.setEnabled(bool(group_name))
        self.category_manager.load_categories(group_name)
        self.skill_manager.clear_skills()
        self.skill_manager.setEnabled(False)
        self.add_tab_btn.setEnabled(False)
        self.group_changed.emit(group_name)
    
    def _on_category_changed(self, category_name: str):
        """カテゴリー変更時の処理"""
        group_name = self.group_combo.currentText()
        self.skill_manager.setEnabled(bool(category_name))
        if category_name:
            self.skill_manager.load_skills(group_name, category_name)
        else:
            self.skill_manager.clear_skills()
        self.add_tab_btn.setEnabled(bool(category_name))

    def get_selected_group(self) -> str:
        """選択中のグループ名を取得"""
        return self.group_combo.currentText()
    
    def get_selected_category(self) -> str:
        """選択中のカテゴリー名を取得"""
        return self.category_manager.get_selected_category()

    # ... (残りのメソッドは変更なし)

