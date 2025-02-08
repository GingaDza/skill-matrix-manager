"""システム管理ウィジェット"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel,
    QListWidget, QTreeWidget, QTreeWidgetItem,
    QComboBox, QSpacerItem, QSizePolicy,
    QScrollArea, QFrame, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt
from .group_manager import GroupManager
from .category_manager import CategoryManager
from ..data_management import DataManagementWidget
from ..custom_tab import CategoryTab
from ...database.database_manager import DatabaseManager
import platform
import logging

class SystemInformationTab(QWidget):
    """システム情報タブ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # スクロール可能なエリアを作成
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content = QWidget()
        content_layout = QVBoxLayout()
        
        # アプリケーション情報
        app_group = QFrame()
        app_group.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        app_layout = QVBoxLayout()
        
        app_layout.addWidget(QLabel("<h2>アプリケーション情報</h2>"))
        app_layout.addWidget(QLabel("スキルマトリックスマネージャー"))
        app_layout.addWidget(QLabel("バージョン: 1.0.0"))
        app_layout.addWidget(QLabel("開発者: GingaDza"))
        
        app_group.setLayout(app_layout)
        content_layout.addWidget(app_group)
        
        # システム情報
        sys_group = QFrame()
        sys_group.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        sys_layout = QVBoxLayout()
        
        sys_layout.addWidget(QLabel("<h2>システム情報</h2>"))
        sys_layout.addWidget(QLabel(f"OS: {platform.system()} {platform.release()}"))
        sys_layout.addWidget(QLabel(f"マシン: {platform.machine()}"))
        
        sys_group.setLayout(sys_layout)
        content_layout.addWidget(sys_group)
        
        # データベース情報
        db_group = QFrame()
        db_group.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        db_layout = QVBoxLayout()
        
        db_layout.addWidget(QLabel("<h2>データベース情報</h2>"))
        db_layout.addWidget(QLabel("データベース: SQLite3"))
        db_layout.addWidget(QLabel("ファイル: skill_matrix.db"))
        
        db_group.setLayout(db_layout)
        content_layout.addWidget(db_group)
        
        # 将来の拡張情報
        future_group = QFrame()
        future_group.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        future_layout = QVBoxLayout()
        
        future_layout.addWidget(QLabel("<h2>将来の拡張</h2>"))
        future_layout.addWidget(QLabel("AssignMeアプリとの連携"))
        future_layout.addWidget(QLabel("- スキルマトリクスの定量化データのエクスポート"))
        future_layout.addWidget(QLabel("- 配置最適化のためのデータ提供"))
        future_layout.addWidget(QLabel("- APIを通じたリアルタイム連携"))
        
        future_group.setLayout(future_layout)
        content_layout.addWidget(future_group)
        
        # 余白を追加
        content_layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.setLayout(layout)

class SystemManagementWidget(QWidget):
    """システム管理ウィジェットクラス"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self._db = db_manager
        self._init_ui()
    
    def _init_ui(self):
        """UIの初期化"""
        layout = QVBoxLayout()
        
        # タブウィジェット
        tab_widget = QTabWidget()
        
        # 初期設定タブ
        settings_tab = QWidget()
        settings_layout = QHBoxLayout()
        
        # グループ管理
        group_manager = GroupManager(self._db)
        settings_layout.addWidget(group_manager)
        
        # カテゴリー管理
        category_manager = CategoryManager(self._db)
        settings_layout.addWidget(category_manager)
        
        settings_tab.setLayout(settings_layout)
        tab_widget.addTab(settings_tab, "初期設定")
        
        # データ管理タブ
        data_tab = DataManagementWidget(self._db)
        tab_widget.addTab(data_tab, "データ管理")
        
        # システム情報タブ
        system_info_tab = SystemInformationTab()
        tab_widget.addTab(system_info_tab, "システム情報")
        
        layout.addWidget(tab_widget)
        
        # 新規タブ追加ボタン
        add_tab_btn = QPushButton("選択したカテゴリーで新規タブを追加")
        add_tab_btn.clicked.connect(self._add_custom_tab)
        layout.addWidget(add_tab_btn)
        
        self.setLayout(layout)
    
    def _add_custom_tab(self):
        """新規カスタムタブを追加"""
        try:
            # カテゴリー選択ダイアログを表示
            selected_category = None  # TODO: カテゴリー選択ダイアログを実装
            if not selected_category:
                return
                
            # メインウィンドウのタブウィジェットにカスタムタブを追加
            main_window = self.window()
            if main_window:
                main_window.add_custom_tab(
                    selected_category,
                    CategoryTab(self._db, selected_category)
                )
                self.logger.info(f"新規タブを追加しました: {selected_category}")
        except Exception as e:
            self.logger.exception("新規タブの追加に失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"新規タブの追加に失敗しました: {str(e)}"
            )
