"""アプリケーションメインモジュール"""
import sys
import logging
import gc
from typing import Optional

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from .views.main_window import MainWindow
from .database.database_manager import DatabaseManager

class SkillMatrixApp(QApplication):
    """スキルマトリックスアプリケーション"""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("アプリケーションを初期化中...")
        
        try:
            self._configure_application()
            self._init_main_window()
            
        except Exception as e:
            self.logger.exception("初期化エラー")
            raise

    def _configure_application(self):
        """アプリケーションの設定"""
        # プラットフォーム固有の設定
        if sys.platform == 'darwin':
            self.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
            self.setAttribute(Qt.ApplicationAttribute.AA_MacDontSwapCtrlAndMeta)
        
        # 一般的な設定
        self.setStyle('Fusion')
        self.setQuitOnLastWindowClosed(True)
        
        # GC設定
        gc.set_threshold(700, 10, 5)

    def _init_main_window(self):
        """メインウィンドウの初期化"""
        try:
            self._db = DatabaseManager()
            self._main_window = MainWindow(self._db)
            self._main_window.show()
            
        except Exception as e:
            self.logger.exception("メインウィンドウの初期化に失敗")
            raise

    def exec(self) -> int:
        """アプリケーションの実行"""
        try:
            return super().exec()
        except Exception as e:
            self.logger.exception("実行時エラー")
            return 1
        finally:
            self._cleanup()

    def _cleanup(self):
        """クリーンアップ処理"""
        try:
            if hasattr(self, '_main_window'):
                self._main_window.close()
                self._main_window.deleteLater()
            
            if hasattr(self, '_db'):
                self._db = None
            
            gc.collect()
            
        except Exception as e:
            self.logger.exception("クリーンアップエラー")

def App(argv=None) -> Optional[SkillMatrixApp]:
    """アプリケーションインスタンスの生成"""
    if argv is None:
        argv = sys.argv
    
    try:
        return SkillMatrixApp(argv)
    except Exception as e:
        logging.exception("アプリケーション作成エラー")
        return None
