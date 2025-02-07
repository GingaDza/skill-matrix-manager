from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLabel, QComboBox
)
from PyQt6.QtCore import pyqtSignal, Qt
import logging

class LeftPane(QWidget):
    """左ペインコンポーネント"""
    group_changed = pyqtSignal(int)  # グループ変更シグナル
    add_user_clicked = pyqtSignal()  # ユーザー追加シグナル
    edit_user_clicked = pyqtSignal()  # ユーザー編集シグナル
    delete_user_clicked = pyqtSignal()  # ユーザー削除シグナル

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing LeftPane")
        
        # UIコンポーネント
        self.group_combo = None
        self.user_list = None
        self.buttons = {}
        
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """UIの初期化"""
        self.logger.debug("Setting up LeftPane UI")
        try:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)

            # グループ選択
            group_label = QLabel("グループ選択:")
            self.group_combo = QComboBox()
            self.group_combo.setObjectName("group_combo")

            # ユーザーリスト
            user_label = QLabel("ユーザー一覧:")
            self.user_list = QListWidget()
            self.user_list.setObjectName("user_list")

            # ボタン
            self.buttons = {
                'add': QPushButton("ユーザー追加"),
                'edit': QPushButton("ユーザー編集"),
                'delete': QPushButton("ユーザー削除")
            }

            # ボタンの設定
            for key, button in self.buttons.items():
                button.setObjectName(f"{key}_button")

            # レイアウトに追加
            layout.addWidget(group_label)
            layout.addWidget(self.group_combo)
            layout.addWidget(user_label)
            layout.addWidget(self.user_list)
            for button in self.buttons.values():
                layout.addWidget(button)
            layout.addStretch()

            self.logger.debug("LeftPane UI setup completed")

        except Exception as e:
            self.logger.error(f"Error setting up LeftPane UI: {e}", exc_info=True)
            raise

    def _connect_signals(self):
        """シグナルの接続"""
        self.logger.debug("Connecting LeftPane signals")
        try:
            # グループ選択の変更
            self.group_combo.currentIndexChanged.connect(self._on_group_changed)

            # ボタンクリック
            self.buttons['add'].clicked.connect(self._on_add_clicked)
            self.buttons['edit'].clicked.connect(self._on_edit_clicked)
            self.buttons['delete'].clicked.connect(self._on_delete_clicked)

            self.logger.debug("LeftPane signals connected")

        except Exception as e:
            self.logger.error(f"Error connecting LeftPane signals: {e}", exc_info=True)
            raise

    def _on_group_changed(self, index):
        """グループ選択変更時の処理"""
        self.logger.debug(f"Group selection changed to index: {index}")
        self.group_changed.emit(index)

    def _on_add_clicked(self):
        """追加ボタンクリック時の処理"""
        self.logger.debug("Add user button clicked")
        self.add_user_clicked.emit()

    def _on_edit_clicked(self):
        """編集ボタンクリック時の処理"""
        self.logger.debug("Edit user button clicked")
        self.edit_user_clicked.emit()

    def _on_delete_clicked(self):
        """削除ボタンクリック時の処理"""
        self.logger.debug("Delete user button clicked")
        self.delete_user_clicked.emit()

    def get_selected_user(self):
        """選択中のユーザー情報を取得"""
        return self.user_list.currentItem()

    def get_current_group_id(self):
        """現在選択中のグループIDを取得"""
        return self.group_combo.currentData()

    def update_button_states(self):
        """ボタンの有効/無効状態を更新"""
        has_selection = bool(self.get_selected_user())
        self.buttons['edit'].setEnabled(has_selection)
        self.buttons['delete'].setEnabled(has_selection)

    def cleanup(self):
        """リソースのクリーンアップ"""
        self.logger.debug("Cleaning up LeftPane")
        try:
            # シグナル接続の解除
            self.group_combo.currentIndexChanged.disconnect()
            for button in self.buttons.values():
                button.clicked.disconnect()
            
            # コンポーネントのクリア
            self.group_combo.clear()
            self.user_list.clear()
            self.buttons.clear()

        except Exception as e:
            self.logger.error(f"Error during LeftPane cleanup: {e}", exc_info=True)
