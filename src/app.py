"""アプリケーションメインモジュール"""
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QtMsgType
from .utils.memory_profiler import MemoryProfiler
from .utils.log_config import memory_loggerfrom .utils.type_manager import TypeManager
import logging
import sys
import psutil
import gc
from typing import Optional
from .views.main_window import MainWindow
from .database.database_manager import DatabaseManager

class SkillMatrixApp(QApplication):
    """スキルマトリックスアプリケーション"""
    
    def __init__(self, argv):
        # デバッグモードの設定
        memory_logger.set_debug_mode(False)  # 通常モードではFalse        super().__init__(argv)
        
        # ロガーの設定
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Starting App initialization")
        
        # メモリプロファイラーの初期化
        self._profiler = MemoryProfiler()
        self._profiler.take_snapshot()
        
        # 型管理システムの初期化
        self._type_manager = TypeManager()
        self.logger.debug("Type manager initialized")
        
        # macOS固有の設定
        self._configure_macos()
        self.logger.debug("App parent initialization complete")
        
        # アプリケーション設定
        self._configure_application()
        self.logger.debug("Application configuration complete")
        
        # メインウィンドウの初期化
        self.logger.debug("Starting application main window")
        self._init_main_window()

    def _configure_macos(self):
        """macOS固有の設定"""
        try:
            if sys.platform == 'darwin':
                self.logger.debug("Configuring macOS specific settings")
                self.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
                self.setAttribute(Qt.ApplicationAttribute.AA_MacDontSwapCtrlAndMeta)
                self.setAttribute(Qt.ApplicationAttribute.AA_DisableWindowContextHelpButton)
        except Exception as e:
            self.logger.error(f"macOS設定エラー: {e}")

    def _configure_application(self):
        """アプリケーションの設定"""
        try:
            # アプリケーション全体の設定
            self.setQuitOnLastWindowClosed(True)
            self.setStyle('Fusion')
            
            # イベントフィルターのインストール
            self.installEventFilter(self)
            
            # GCの設定
            gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_STATS)
            gc.set_threshold(700, 10, 5)
            
            self.logger.debug("Application configuration complete")
            
        except Exception as e:
            self.logger.error(f"アプリケーション設定エラー: {e}")

    def _init_main_window(self):
        """メインウィンドウの初期化"""
        try:
            self._db = DatabaseManager()
            self._main_window = MainWindow(self._db)
            self._main_window.show()
            
        except Exception as e:
            self.logger.error(f"メインウィンドウ初期化エラー: {e}")
            raise

    def notify(self, receiver, event) -> bool:
        """イベント通知のオーバーライド"""
        try:
            return super().notify(receiver, event)
        except Exception as e:
            self.logger.error(f"イベント通知エラー: {e}")
            return False

    def event(self, event) -> bool:
        """イベントフィルター"""
        try:
            # メモリ使用量の監視
            if event.type() == Qt.ApplicationAttribute.AA_EnableHighDpiScaling:
                process = psutil.Process()
                mem = process.memory_full_info()
                rss_mb = mem.rss / (1024 * 1024)
                vms_mb = mem.vms / (1024 * 1024)
                
                if vms_mb > 512:  # 512MB以上
                    self.logger.warning(f"高メモリ使用量: VMS {vms_mb:.1f}MB")
                    gc.collect()
            
            return super().event(event)
            
        except Exception as e:
            self.logger.error(f"イベントフィルターエラー: {e}")
            return False

    def handle_message(self, msg_type: QtMsgType, msg: str):
        """メッセージハンドリング"""
        try:
            if msg_type == QtMsgType.QtDebugMsg:
                self.logger.debug(msg)
            elif msg_type == QtMsgType.QtInfoMsg:
                self.logger.info(msg)
            elif msg_type == QtMsgType.QtWarningMsg:
                self.logger.warning(msg)
            elif msg_type == QtMsgType.QtCriticalMsg:
                self.logger.error(msg)
            elif msg_type == QtMsgType.QtFatalMsg:
                self.logger.critical(msg)
                
        except Exception as e:
            self.logger.error(f"メッセージハンドリングエラー: {e}")

    def cleanup(self):
        """アプリケーションのクリーンアップ"""
        try:
            # メモリリークの検出
            leaks = self._profiler.find_memory_leaks()
            if leaks:
                self.logger.warning("メモリリーク検出:")
                for leak in leaks:
                    self.logger.warning(f"  {leak}")
            
            # 型管理システムのクリーンアップ
            self._type_manager.cleanup()
            self.logger.debug("Type manager cleaned up")
            
            # プロファイラーのクリーンアップ
            self._profiler.cleanup()
            
            # 最終的なガベージコレクション
            gc.collect()
            
        except Exception as e:
            self.logger.error(f"クリーンアップエラー: {e}")

def App(argv=None) -> Optional[SkillMatrixApp]:
    """アプリケーションインスタンスの取得"""
    if argv is None:
        argv = sys.argv
        
    try:
        return SkillMatrixApp(argv)
    except Exception as e:
        logging.error(f"アプリケーション初期化エラー: {e}")
        return None
