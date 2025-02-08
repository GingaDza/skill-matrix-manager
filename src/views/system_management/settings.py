"""初期設定ウィジェット"""
import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QListWidget, QPushButton,
    QInputDialog, QMessageBox, QLabel, QComboBox
)
from PyQt6.QtCore import Qt
from ...database.database_manager import DatabaseManager

class SettingsWidget(QWidget):
    """初期設定タブのウィジェット"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        
        # UI要素の初期化
        self.group_list = None
        self.category_group_combo = None
        self.parent_list = None
        self.child_list = None
        
        # ボタンの初期化
        self.add_group_btn = None
        self.edit_group_btn = None
        self.delete_group_btn = None
        self.add_category_btn = None
        self.edit_category_btn = None
        self.delete_category_btn = None
        self.add_skill_btn = None
        self.edit_skill_btn = None
        self.delete_skill_btn = None
        self.new_tab_btn = None
        
        # UIの構築
        self._init_ui()
        self._connect_signals()
        self._load_data()

    def _init_ui(self):
        """UIの初期化"""
        layout = QHBoxLayout()
        
        # グループリスト
        group_box = self._create_group_list()
        layout.addWidget(group_box)
        
        # カテゴリーリスト
        category_box = self._create_category_lists()
        layout.addWidget(category_box)
        
        self.setLayout(layout)

    def _create_group_list(self):
        """グループリストの作成"""
        group_box = QGroupBox("グループリスト")
        layout = QVBoxLayout()
        
        self.group_list = QListWidget()
        layout.addWidget(self.group_list)
        
        # 操作ボタン
        button_layout = QVBoxLayout()
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        
        button_layout.addWidget(self.add_group_btn)
        button_layout.addWidget(self.edit_group_btn)
        button_layout.addWidget(self.delete_group_btn)
        
        layout.addLayout(button_layout)
        group_box.setLayout(layout)
        return group_box

    def _create_category_lists(self):
        """カテゴリーリストの作成"""
        category_box = QGroupBox("カテゴリー管理")
        layout = QVBoxLayout()
        
        # グループ選択
        group_select_layout = QHBoxLayout()
        group_select_layout.addWidget(QLabel("グループ:"))
        self.category_group_combo = QComboBox()
        group_select_layout.addWidget(self.category_group_combo)
        layout.addLayout(group_select_layout)
        
        # 親カテゴリー
        parent_box = QGroupBox("親カテゴリー")
        parent_layout = QVBoxLayout()
        self.parent_list = QListWidget()
        parent_layout.addWidget(self.parent_list)
        parent_box.setLayout(parent_layout)
        
        # 子カテゴリー
        child_box = QGroupBox("子カテゴリー")
        child_layout = QVBoxLayout()
        self.child_list = QListWidget()
        child_layout.addWidget(self.child_list)
        child_box.setLayout(child_layout)
        
        layout.addWidget(parent_box)
        layout.addWidget(child_box)
        
        # 操作ボタン
        button_layout = QVBoxLayout()
        self.add_category_btn = QPushButton("カテゴリー追加")
        self.edit_category_btn = QPushButton("カテゴリー編集")
        self.delete_category_btn = QPushButton("カテゴリー削除")
        self.add_skill_btn = QPushButton("スキル追加")
        self.edit_skill_btn = QPushButton("スキル編集")
        self.delete_skill_btn = QPushButton("スキル削除")
        self.new_tab_btn = QPushButton("新規タブ追加")
        
        button_layout.addWidget(self.add_category_btn)
        button_layout.addWidget(self.edit_category_btn)
        button_layout.addWidget(self.delete_category_btn)
        button_layout.addWidget(self.add_skill_btn)
        button_layout.addWidget(self.edit_skill_btn)
        button_layout.addWidget(self.delete_skill_btn)
        button_layout.addWidget(self.new_tab_btn)
        
        layout.addLayout(button_layout)
        category_box.setLayout(layout)
        return category_box

    def _connect_signals(self):
        """シグナルの接続"""
        # グループ操作
        self.add_group_btn.clicked.connect(self._add_group)
        self.edit_group_btn.clicked.connect(self._edit_group)
        self.delete_group_btn.clicked.connect(self._delete_group)
        
        # カテゴリー操作
        self.add_category_btn.clicked.connect(self._add_category)
        self.edit_category_btn.clicked.connect(self._edit_category)
        self.delete_category_btn.clicked.connect(self._delete_category)
        
        # スキル操作
        self.add_skill_btn.clicked.connect(self._add_skill)
        self.edit_skill_btn.clicked.connect(self._edit_skill)
        self.delete_skill_btn.clicked.connect(self._delete_skill)
        
        # タブ操作
        self.new_tab_btn.clicked.connect(self._add_new_tab)
        
        # リスト選択
        self.parent_list.currentRowChanged.connect(self._on_parent_selected)
        self.category_group_combo.currentTextChanged.connect(self._on_category_group_changed)
        self.group_list.currentRowChanged.connect(self._on_group_selected)

    def _load_data(self):
        """データの読み込み"""
        try:
            # グループの読み込み
            groups = self._db_manager.get_groups()
            
            # グループリストの更新
            self.group_list.clear()
            self.group_list.addItems(groups)
            
            # グループコンボボックスの更新
            self.category_group_combo.clear()
            self.category_group_combo.addItems(groups)
            
        except Exception as e:
            self.logger.exception("データ読み込みエラー")
            QMessageBox.critical(
                self,
                "エラー",
                "データの読み込みに失敗しました。"
            )

    # [その他のメソッドは前回と同じ]

