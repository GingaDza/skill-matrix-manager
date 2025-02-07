from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import QObject, Qt, QTimer, QMetaObject, QCoreApplication, QThread
import logging
import traceback
from typing import Optional, Dict, Any, List, Tuple
import psutil
import json
import os
import gc
import sys
from datetime import datetime

class DataHandler(QObject):
    """データ操作を管理するハンドラー"""
    # メモリ制限をより厳格に設定
    MAX_MEMORY_RSS_MB = 150
    MAX_MEMORY_VMS_MB = 400
    CLEANUP_THRESHOLD_MB = 100
    UPDATE_INTERVAL_MS = 250  # 更新間隔を延長

    def __init__(self, db, main_window):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        # 基本設定
        self.db = db
        self._main_window = main_window
        self.is_updating = False
        
        # メモリ管理
        self._update_count = 0
        self._last_cleanup = datetime.now()
        
        # 状態管理
        self._last_group_id = None
        self._last_user_id = None
        self._update_depth = 0
        self._cache = {}
        
        # 更新管理
        self._setup_timers()
        self._setup_debug()

    def _setup_timers(self):
        """タイマーの初期化"""
        # 更新タイマー
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._safe_process_update)
        
        # メモリチェックタイマー
        self._memory_timer = QTimer()
        self._memory_timer.timeout.connect(self._check_memory)
        self._memory_timer.start(3000)  # 3秒ごとにチェック

    def _setup_debug(self):
        """デバッグ環境の設定"""
        self.logger.setLevel(logging.DEBUG)
        debug_dir = os.path.join('debug_logs', datetime.now().strftime('%Y%m%d'))
        os.makedirs(debug_dir, exist_ok=True)
        
        handler = logging.FileHandler(
            os.path.join(debug_dir, f'data_handler_{datetime.now().strftime("%H%M%S")}.log'),
            encoding='utf-8'
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        
        self._initial_memory = self._get_memory_usage()
        self._log_state("初期化完了")

    def _get_memory_usage(self) -> Dict[str, float]:
        """メモリ使用状況の取得"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            return {
                'rss': memory_info.rss / (1024 * 1024),
                'vms': memory_info.vms / (1024 * 1024)
            }
        except Exception as e:
            self.logger.error(f"メモリ情報取得エラー: {e}")
            return {'rss': 0.0, 'vms': 0.0}

    def _log_state(self, action: str):
        """現在の状態をログに記録"""
        try:
            current = self._get_memory_usage()
            diff = {k: current[k] - self._initial_memory[k] for k in current}
            
            self.logger.debug(
                f"State ({action}):\n"
                f"  メモリ RSS: {current['rss']:.1f}MB (変化: {diff['rss']:+.1f}MB)\n"
                f"  メモリ VMS: {current['vms']:.1f}MB (変化: {diff['vms']:+.1f}MB)\n"
                f"  更新回数: {self._update_count}\n"
                f"  キャッシュサイズ: {len(self._cache)}\n"
                f"  更新深度: {self._update_depth}"
            )
        except Exception as e:
            self.logger.error(f"状態ログ記録エラー: {e}")

    def _check_memory(self):
        """メモリ使用状況のチェックと対応"""
        try:
            current = self._get_memory_usage()
            
            if (current['rss'] > self.MAX_MEMORY_RSS_MB or
                current['vms'] > self.MAX_MEMORY_VMS_MB):
                self.logger.warning("メモリ使用量超過")
                self._emergency_cleanup()
                
            elif current['rss'] > self.CLEANUP_THRESHOLD_MB:
                self.logger.info("メモリ使用量警告")
                self._cleanup_cache()
                
        except Exception as e:
            self.logger.error(f"メモリチェックエラー: {e}")

    def _emergency_cleanup(self):
        """緊急メモリクリーンアップ"""
        try:
            self.logger.info("緊急クリーンアップ開始")
            
            # キャッシュクリア
            self._cache.clear()
            
            # 明示的なガベージコレクション
            gc.collect()
            
            # システムメモリの解放要求
            if hasattr(sys, 'set_asyncgen_hooks'):
                sys.set_asyncgen_hooks(None, None)
            
            self._log_state("緊急クリーンアップ完了")
            
        except Exception as e:
            self.logger.error(f"緊急クリーンアップエラー: {e}")

    def _cleanup_cache(self):
        """通常のキャッシュクリーンアップ"""
        try:
            self._cache.clear()
            gc.collect()
            self._log_state("キャッシュクリーンアップ完了")
        except Exception as e:
            self.logger.error(f"キャッシュクリーンアップエラー: {e}")

    def schedule_update(self, immediate: bool = False):
        """更新のスケジュール"""
        try:
            if self._update_depth > 3:  # 深度制限を厳格化
                self.logger.warning("更新深度制限超過")
                return
            
            interval = 0 if immediate else self.UPDATE_INTERVAL_MS
            self._update_timer.start(interval)
            self._log_state("更新スケジュール")
            
        except Exception as e:
            self.logger.error(f"更新スケジュールエラー: {e}")

    def _safe_process_update(self):
        """安全な更新処理の実行"""
        if self.is_updating:
            return

        try:
            self.is_updating = True
            self._update_count += 1
            self._update_depth += 1
            
            # メモリチェック
            self._check_memory()
            
            # UI更新
            if self._main_window and hasattr(self._main_window, 'left_pane'):
                self._update_ui()
            
            self._log_state("更新完了")
            
        except Exception as e:
            self.logger.error(f"更新処理エラー: {e}")
            self._show_error("データ更新エラー")
        finally:
            self._update_depth -= 1
            self.is_updating = False

    def _update_ui(self):
        """UI要素の更新"""
        try:
            left_pane = self._main_window.left_pane
            
            # グループ更新
            groups = self.db.get_all_groups()
            current_group_id = self._last_group_id or left_pane.get_current_group_id()
            
            left_pane.group_combo.blockSignals(True)
            try:
                left_pane.group_combo.clear()
                for group_id, group_name in groups:
                    left_pane.group_combo.addItem(group_name, group_id)
                
                if current_group_id:
                    index = left_pane.group_combo.findData(current_group_id)
                    if index >= 0:
                        left_pane.group_combo.setCurrentIndex(index)
                        self._last_group_id = current_group_id
            finally:
                left_pane.group_combo.blockSignals(False)
            
            # ユーザー更新
            if self._last_group_id:
                users = self.db.get_users_by_group(self._last_group_id)
                current_row = left_pane.user_list.currentRow()
                
                left_pane.user_list.blockSignals(True)
                try:
                    left_pane.user_list.clear()
                    for user_id, user_name in users:
                        item = QListWidgetItem(user_name)
                        item.setData(Qt.ItemDataRole.UserRole, user_id)
                        left_pane.user_list.addItem(item)
                    
                    if 0 <= current_row < left_pane.user_list.count():
                        left_pane.user_list.setCurrentRow(current_row)
                finally:
                    left_pane.user_list.blockSignals(False)
            
            left_pane.update_button_states()
            
        except Exception as e:
            self.logger.error(f"UI更新エラー: {e}")
            raise

    def _show_error(self, message: str):
        """エラーメッセージの表示"""
        try:
            QMessageBox.critical(None, "エラー", message)
        except Exception as e:
            self.logger.error(f"エラー表示失敗: {e}")

    def cleanup(self):
        """終了時のクリーンアップ"""
        try:
            self._log_state("終了処理開始")
            
            # タイマーの停止
            self._update_timer.stop()
            self._memory_timer.stop()
            
            # リソースの解放
            self._cache.clear()
            self._main_window = None
            self.db = None
            
            # 最終クリーンアップ
            gc.collect()
            
            self._log_state("終了処理完了")
            
        except Exception as e:
            self.logger.error(f"終了処理エラー: {e}")

    def load_initial_data(self):
        """初期データの読み込み"""
        self.logger.debug("初期データ読み込み開始")
        self.schedule_update(immediate=True)

    def refresh_data(self):
        """データの更新をリクエスト"""
        self.logger.debug("データ更新リクエスト受信")
        self.schedule_update()

    def refresh_user_list(self):
        """ユーザーリストの更新をリクエスト"""
        self.logger.debug("ユーザーリスト更新リクエスト受信")
        if not self.is_updating and self._last_group_id:
            self._update_ui()
