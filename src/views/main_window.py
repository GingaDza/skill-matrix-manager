"""メインウィンドウモジュール"""
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QTabWidget,
    QComboBox, QMessageBox, QFrame, QSplitter,
    QGroupBox
)
from PyQt6.QtCore import Qt
from ..database.database_manager import DatabaseManager
from .system_management import SystemManagementWidget

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()

    def _init_ui(self):
        """UIの初期化"""
        self.setWindowTitle("スキルマトリックス管理")
        self.setMinimumSize(1200, 800)

        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # メインレイアウト
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # 3:7のスプリッター
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左ペイン (3)
        left_pane = self._create_left_pane()
        splitter.addWidget(left_pane)
        
        # 右ペイン (7)
        right_pane = self._create_right_pane()
        splitter.addWidget(right_pane)
        
        # スプリッター比率設定
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)
        
        main_layout.addWidget(splitter)

        # デバッグ用：初期データの読み込みを確認
        self.logger.info("初期データの読み込みを開始")
        self._load_initial_data()

    def _create_left_pane(self):
        """左ペインの作成"""
        widget = QWidget(self)
        layout = QVBoxLayout()
        
        # グループ選択
        group_box = QGroupBox("グループ管理", widget)
        group_layout = QVBoxLayout()
        
        self.group_combo = QComboBox()
        group_layout.addWidget(self.group_combo)
        
        # ユーザーリスト
        self.user_list = QListWidget()
        group_layout.addWidget(self.user_list)
        
        # 操作ボタン
        button_layout = QVBoxLayout()
        add_user_btn = QPushButton("追加")
        edit_user_btn = QPushButton("編集")
        delete_user_btn = QPushButton("削除")
        
        button_layout.addWidget(add_user_btn)
        button_layout.addWidget(edit_user_btn)
        button_layout.addWidget(delete_user_btn)
        
        group_layout.addLayout(button_layout)
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        
        # シグナル接続
        self.group_combo.currentTextChanged.connect(self._on_user_group_changed)
        
        widget.setLayout(layout)
        return widget

    def _create_right_pane(self):
        """右ペインの作成"""
        widget = QWidget(self)
        layout = QVBoxLayout()
        
        # タブウィジェット
        self.tab_widget = QTabWidget(widget)
        
        # システム管理タブ
        system_tab = SystemManagementWidget(self._db_manager, self.tab_widget)
        self.tab_widget.addTab(system_tab, "システム管理")
        
        layout.addWidget(self.tab_widget)
        widget.setLayout(layout)
        return widget

    def _load_initial_data(self):
        """初期データの読み込み"""
        try:
            # グループの読み込み
            groups = self._db_manager.get_groups()
            self.logger.info(f"読み込まれたグループ: {groups}")
            
            # グループコンボボックスの更新
            self.group_combo.clear()
            self.group_combo.addItems(groups)
            
            # 最初のグループのユーザーを表示
            if groups:
                self._on_user_group_changed(groups[0])
                
        except Exception as e:
            self.logger.exception("初期データ読み込みエラー")
            QMessageBox.critical(
                self,
                "エラー",
                "初期データの読み込みに失敗しました。"
            )

    def _on_user_group_changed(self, group_name: str):
        """ユーザーリストのグループ変更時の処理"""
        try:
            if group_name:
                self.logger.info(f"選択されたグループ: {group_name}")
                users = self._db_manager.get_users_by_group(group_name)
                self.logger.info(f"グループのユーザー: {users}")
                
                self.user_list.clear()
                self.user_list.addItems(users)
                
        except Exception as e:
            self.logger.exception("ユーザーリスト更新エラー")

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        try:
            reply = QMessageBox.question(
                self,
                "確認",
                "アプリケーションを終了しますか？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
                
        except Exception as e:
            self.logger.exception("終了処理エラー")
            event.accept()
