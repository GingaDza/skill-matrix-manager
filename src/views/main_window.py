[前のコードと同じ内容...]

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("Starting MainWindow initialization")
        
        if not QCoreApplication.instance():
            self.logger.critical("QApplication not created before MainWindow")
            raise RuntimeError("QApplication must be created before MainWindow")
            
        super().__init__()
        self.logger.debug("MainWindow parent initialization complete")
        
        # クラッシュ時のスタックトレース出力を設定
        sys.excepthook = self._exception_hook
        
        # メモリ管理の追跡
        self._debug_refs = set()
        
        self._initialize_components()
        self._setup_ui()
        self._connect_signals()
        
        # 初期データ読み込み
        QTimer.singleShot(100, self._safe_initial_load)

    def _safe_initial_load(self):
        """安全な初期データ読み込み"""
        self.logger.debug("Starting safe initial load")
        try:
            self.data_handler.load_initial_data()
        except Exception as e:
            self.logger.error(f"Error in initial load: {e}", exc_info=True)
            QMessageBox.critical(self, "エラー", "初期データの読み込みに失敗しました")

    def _track_ref(self, obj):
        """オブジェクト参照の追跡"""
        self._debug_refs.add(obj)
        self.logger.debug(f"Tracking new object: {obj.__class__.__name__}")

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        self.logger.debug("Processing window close event")
        try:
            # クリーンアップ
            self._cleanup()
            self.window_closed.emit()
            self.logger.debug("Window closed signal emitted")
        except Exception as e:
            self.logger.error(f"Error in close event: {e}", exc_info=True)
        finally:
            event.accept()

    def _cleanup(self):
        """リソースのクリーンアップ"""
        self.logger.debug("Starting cleanup")
        try:
            # タイマーの停止
            if hasattr(self, 'refresh_timer'):
                self.refresh_timer.stop()
            
            # 参照の解放
            self._debug_refs.clear()
            
            self.logger.debug("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}", exc_info=True)

[残りのコードは同じ...]
