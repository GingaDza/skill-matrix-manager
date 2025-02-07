from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea,
    QGridLayout, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import logging
from typing import Optional, Dict, Any, List

class RightPane(QWidget):
    """右ペインコンポーネント"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing RightPane")
        
        super().__init__()
        self._setup_ui()
        self._setup_signals()
        
        # 状態管理
        self._current_user_id: Optional[int] = None
        self._skill_widgets: Dict[int, List[QWidget]] = {}

    def _setup_ui(self):
        """UIコンポーネントの設定"""
        self.logger.debug("Setting up RightPane UI")
        
        # メインレイアウト
        layout = QVBoxLayout()
        
        # ユーザー情報セクション
        user_info_layout = QHBoxLayout()
        self.user_name_label = QLabel("ユーザー未選択")
        user_info_layout.addWidget(self.user_name_label)
        
        # スキルマトリクスセクション
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.skill_container = QWidget()
        self.skill_layout = QGridLayout()
        self.skill_container.setLayout(self.skill_layout)
        
        scroll_area.setWidget(self.skill_container)
        
        # レイアウトの組み立て
        layout.addLayout(user_info_layout)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
        self.logger.debug("RightPane UI setup completed")

    def _setup_signals(self):
        """内部シグナルの設定"""
        self.logger.debug("Setting up internal signals")
        
        # 内部シグナルの設定（必要に応じて）
        self.logger.debug("Internal signals setup completed")

    def connect_signals(self, handler):
        """外部シグナルの接続"""
        self.logger.debug("Connecting external signals")
        
        # イベントハンドラーへの接続
        self._event_handler = handler
        
        self.logger.debug("External signals connected")

    def update_user_info(self, user_id: int, user_name: str):
        """ユーザー情報の更新"""
        self.logger.debug(f"Updating user info: {user_name} (ID: {user_id})")
        
        self._current_user_id = user_id
        self.user_name_label.setText(f"ユーザー: {user_name}")
        
        # スキルマトリクスの更新
        self._clear_skill_matrix()
        self._load_skill_matrix()

    def _clear_skill_matrix(self):
        """スキルマトリクスのクリア"""
        self.logger.debug("Clearing skill matrix")
        
        # 既存のウィジェットを削除
        for widgets in self._skill_widgets.values():
            for widget in widgets:
                self.skill_layout.removeWidget(widget)
                widget.deleteLater()
        
        self._skill_widgets.clear()

    def _load_skill_matrix(self):
        """スキルマトリクスの読み込み"""
        if not self._current_user_id:
            return
            
        self.logger.debug(f"Loading skill matrix for user {self._current_user_id}")
        
        try:
            # ここでスキルマトリクスのデータを読み込む
            # 現在は仮の実装
            pass
            
        except Exception as e:
            self.logger.error(f"Error loading skill matrix: {e}")
            return

    def _create_skill_cell(self, skill_id: int, level: int) -> QWidget:
        """スキルセルの作成"""
        cell = QComboBox()
        cell.addItems(["未評価", "初級", "中級", "上級"])
        cell.setCurrentIndex(level)
        return cell

    def cleanup(self):
        """リソースのクリーンアップ"""
        self.logger.debug("Cleaning up RightPane")
        
        # ウィジェットのクリーンアップ
        self._clear_skill_matrix()
        
        # 参照のクリア
        self._event_handler = None
        self._current_user_id = None
