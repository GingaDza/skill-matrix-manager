"""メインウィンドウの実装"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QMessageBox, QComboBox,
    QListWidget, QLabel, QSplitter
)
from PyQt5.QtCore import Qt
from .system_management import SystemManagementWidget
from ..database.database_manager import DatabaseManager
import logging

class MainWindow(QMainWindow):
    """メインウィンドウクラス"""

    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._db_manager = db_manager
        self._init_ui()
        self.logger.info("初期データの読み込みを開始")

    def _init_ui(self):
        """UIの初期化"""
        self.setWindowTitle('スキルマトリックスマネージャー')
        self.setGeometry(100, 100, 1200, 800)

        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # 3:7の分割を作成
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # 左側のパネル（3割）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # グループ選択
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        self.group_combo.currentTextChanged.connect(self._on_group_changed)
        group_layout.addWidget(self.group_combo)
        left_layout.addLayout(group_layout)
        
        # ユーザーリスト
        self.user_list = QListWidget()
        left_layout.addWidget(self.user_list)
        
        # ユーザー操作ボタン
        button_layout = QVBoxLayout()
        
        add_user_btn = QPushButton("ユーザー追加")
        add_user_btn.clicked.connect(self._add_user)
        button_layout.addWidget(add_user_btn)
        
        edit_user_btn = QPushButton("ユーザー編集")
        edit_user_btn.clicked.connect(self._edit_user)
        button_layout.addWidget(edit_user_btn)
        
        delete_user_btn = QPushButton("ユーザー削除")
        delete_user_btn.clicked.connect(self._delete_user)
        button_layout.addWidget(delete_user_btn)
        
        left_layout.addLayout(button_layout)
        splitter.addWidget(left_panel)

        # 右側のパネル（7割）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # メインタブウィジェット
        self.main_tab_widget = QTabWidget()
        self.main_tab_widget.setMovable(True)  # タブの並び替えを可能にする
        
        # システム管理タブ
        system_tab = SystemManagementWidget(self._db_manager, self)
        self.main_tab_widget.addTab(system_tab, "システム管理")
        
        # 総合評価タブ
        evaluation_tab = QWidget()  # TODO: 総合評価タブの実装
        self.main_tab_widget.addTab(evaluation_tab, "総合評価")
        
        right_layout.addWidget(self.main_tab_widget)
        splitter.addWidget(right_panel)
        
        # スプリッターの比率を3:7に設定
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)

        self._load_groups()

    def _load_groups(self):
        """グループ一覧を読み込む"""
        self.group_combo.clear()
        try:
            groups = self._db_manager.get_groups()
            if groups:
                self.group_combo.addItems(groups)
                self.group_combo.setCurrentIndex(0)
        except Exception as e:
            self.logger.exception("グループの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"グループの読み込みに失敗しました: {str(e)}"
            )

    def _on_group_changed(self, group_name: str):
        """グループ変更時の処理"""
        self._load_users(group_name)

    def _load_users(self, group_name: str):
        """ユーザー一覧を読み込む"""
        self.user_list.clear()
        if not group_name:
            return
            
        try:
            users = self._db_manager.get_users(group_name)
            if users:
                for user in users:
                    self.user_list.addItem(user['name'])
        except Exception as e:
            self.logger.exception("ユーザーの読み込みに失敗しました")
            QMessageBox.critical(
                self,
                "エラー",
                f"ユーザーの読み込みに失敗しました: {str(e)}"
            )

    def _add_user(self):
        """ユーザーを追加する"""
        group_name = self.group_combo.currentText()
        if not group_name:
            QMessageBox.warning(self, "警告", "グループを選択してください")
            return

        from .dialogs import AddUserDialog
        dialog = AddUserDialog(self)
        if dialog.exec_():
            name = dialog.name
            email = dialog.email
            try:
                self._db_manager.add_user(name, group_name, email)
                self._load_users(group_name)
                self.logger.info(f"ユーザーを追加しました: {name} (グループ: {group_name})")
            except Exception as e:
                self.logger.exception("ユーザーの追加に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"ユーザーの追加に失敗しました: {str(e)}"
                )

    def _edit_user(self):
        """ユーザーを編集する"""
        current_item = self.user_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "編集するユーザーを選択してください")
            return

        group_name = self.group_combo.currentText()
        old_name = current_item.text()

        from .dialogs import EditUserDialog
        dialog = EditUserDialog(self, old_name)
        if dialog.exec_():
            new_name = dialog.name
            email = dialog.email
            try:
                self._db_manager.update_user(old_name, new_name, group_name)
                self._load_users(group_name)
                self.logger.info(f"ユーザーを更新しました: {old_name} -> {new_name}")
            except Exception as e:
                self.logger.exception("ユーザーの更新に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"ユーザーの更新に失敗しました: {str(e)}"
                )

    def _delete_user(self):
        """ユーザーを削除する"""
        current_item = self.user_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "削除するユーザーを選択してください")
            return

        group_name = self.group_combo.currentText()
        name = current_item.text()

        reply = QMessageBox.question(
            self,
            "確認",
            f"ユーザー「{name}」を削除してもよろしいですか？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self._db_manager.delete_user(name, group_name)
                self._load_users(group_name)
                self.logger.info(f"ユーザーを削除しました: {name}")
            except Exception as e:
                self.logger.exception("ユーザーの削除に失敗しました")
                QMessageBox.critical(
                    self,
                    "エラー",
                    f"ユーザーの削除に失敗しました: {str(e)}"
                )

    def closeEvent(self, event):
        """ウィンドウを閉じる際の処理"""
        reply = QMessageBox.question(
            self,
            'アプリケーションの終了',
            "アプリケーションを終了しますか？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.logger.info("アプリケーションを終了します")
            event.accept()
        else:
            event.ignore()

    def add_custom_tab(self, title: str, widget: QWidget):
        """カスタムタブを追加"""
        self.main_tab_widget.insertTab(
            self.main_tab_widget.count() - 2,  # 総合評価とシステム管理タブの前
            widget,
            title
        )
