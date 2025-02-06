from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QStatusBar, QLabel
)
from datetime import datetime
from .tabs.system_management.system_management_tab import SystemManagementTab
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, controllers=None):
        super().__init__()
        self.controllers = controllers
        self.current_time = datetime.now()
        self.current_user = "GingaDza"
        
        logger.debug(f"{self.current_time} - {self.current_user} Initializing MainWindow")
        self.initUI()
    
    def initUI(self):
        try:
            # ウィンドウの基本設定
            self.setWindowTitle('スキルマトリクスシステム')
            self.setMinimumSize(1200, 800)
            
            # メインウィジェット
            main_widget = QWidget()
            self.setCentralWidget(main_widget)
            
            # メインレイアウト
            main_layout = QVBoxLayout(main_widget)
            main_layout.setContentsMargins(5, 5, 5, 5)
            
            # タブウィジェットの作成
            self.tab_widget = QTabWidget()
            self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
            self.tab_widget.setMovable(True)
            
            # システム管理タブの追加
            system_management_tab = SystemManagementTab(self.controllers)
            self.tab_widget.addTab(system_management_tab, "システム管理")
            
            # レイアウトにタブウィジェットを追加
            main_layout.addWidget(self.tab_widget)
            
            # ステータスバーの設定
            self.setup_status_bar()
            
            logger.debug(f"{self.current_time} - {self.current_user} MainWindow UI initialization completed")
            
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in MainWindow UI initialization: {e}")
            logger.exception("Detailed traceback:")
            raise

    def setup_status_bar(self):
        try:
            status_bar = QStatusBar()
            self.setStatusBar(status_bar)
            
            user_label = QLabel(f"ユーザー: {self.current_user}")
            status_bar.addWidget(user_label)
            
            time_label = QLabel(f"時刻: {self.current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            status_bar.addPermanentWidget(time_label)
            
            logger.debug(f"{self.current_time} - {self.current_user} Status bar setup completed")
            
        except Exception as e:
            logger.error(f"{self.current_time} - {self.current_user} Error in status bar setup: {e}")
            logger.exception("Detailed traceback:")
            raise
