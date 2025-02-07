import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QLocale, QTimer
import platform
from .views.main_window import MainWindow

class App(QApplication):
    """アプリケーションのメインクラス"""
    def __init__(self, argv):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Starting App initialization")
        
        # macOS特有の設定
        if platform.system() == 'Darwin':
            self.logger.debug("Configuring macOS specific settings")
            # IMKClientのエラーを防ぐ
            argv += ['-platformpluginpath', '/usr/local/Frameworks/QtPlugins/platforms']
            
        super().__init__(argv)
        self.logger.debug("App parent initialization complete")
        
        # アプリケーション全体の設定
        self._configure_application()
        
        # メインウィンドウ
        self.main_window = None
        self.exit_timer = QTimer()
        self.exit_timer.setSingleShot(True)
        self.exit_timer.timeout.connect(self.quit)

    def _configure_application(self):
        """アプリケーション全体の設定"""
        self.logger.debug("Configuring application settings")
        try:
            # プラットフォーム固有の設定
            if platform.system() == 'Darwin':
                self.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus)
                self.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
                
            # 共通設定
            self.setApplicationName("スキルマトリックス管理システム")
            self.setApplicationVersion("1.0.0")
            self.setStyle("Fusion")
            
            # ロケールの設定
            QLocale.setDefault(QLocale(QLocale.Language.Japanese, QLocale.Country.Japan))
            
            self.logger.debug("Application configuration complete")
            
        except Exception as e:
            self.logger.error(f"Error configuring application: {e}", exc_info=True)
            raise

    def start(self):
        """アプリケーションの起動"""
        try:
            self.logger.debug("Starting application main window")
            self.main_window = MainWindow()
            self.main_window.show()
            
            # クリーンアップ設定
            self.main_window.window_closed.connect(self._handle_window_close)
            
            return self.exec()
            
        except Exception as e:
            self.logger.error(f"Error starting application: {e}", exc_info=True)
            return 1

    def _handle_window_close(self):
        """メインウィンドウが閉じられた時の処理"""
        self.logger.debug("Handling window close")
        try:
            # 遅延終了で残りのイベントを処理
            self.exit_timer.start(100)
        except Exception as e:
            self.logger.error(f"Error handling window close: {e}", exc_info=True)
            self.quit()
