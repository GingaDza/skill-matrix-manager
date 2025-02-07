from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QMessageBox, QInputDialog, QComboBox, QTabWidget,
    QSpinBox
)
from PyQt6.QtCore import Qt
from ..database.database_manager import DatabaseManager
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.db = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        """UIの初期設定"""
        self.setWindowTitle("スキルマトリックス管理システム")
        self.setGeometry(100, 100, 1400, 800)

        # メインウィジェット
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 左ペイン (3:7の分割)
        left_pane = self._create_left_pane()
        main_layout.addWidget(left_pane, stretch=3)

        # 右ペイン (タブウィジェット)
        self.tab_widget = self._create_right_pane()
        main_layout.addWidget(self.tab_widget, stretch=7)

        # データの読み込み
        self.load_data()

    def _create_left_pane(self):
        """左ペインの作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # グループ選択
        group_widget = QWidget()
        group_layout = QVBoxLayout(group_widget)
        group_layout.addWidget(QLabel("グループ選択"))
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self.on_group_changed)
        group_layout.addWidget(self.group_combo)
        layout.addWidget(group_widget)

        # ユーザーリスト
        user_widget = QWidget()
        user_layout = QVBoxLayout(user_widget)
        user_layout.addWidget(QLabel("ユーザーリスト"))
        self.user_list = QListWidget()
        self.user_list.itemSelectionChanged.connect(self.on_user_selected)
        user_layout.addWidget(self.user_list)
        layout.addWidget(user_widget)

        # ユーザー操作ボタン
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        
        self.add_user_btn = QPushButton("ユーザー追加")
        self.edit_user_btn = QPushButton("ユーザー編集")
        self.delete_user_btn = QPushButton("ユーザー削除")

        self.add_user_btn.clicked.connect(self.add_user)
        self.edit_user_btn.clicked.connect(self.edit_user)
        self.delete_user_btn.clicked.connect(self.delete_user)

        button_layout.addWidget(self.add_user_btn)
        button_layout.addWidget(self.edit_user_btn)
        button_layout.addWidget(self.delete_user_btn)
        layout.addWidget(button_widget)

        return widget

    def _create_right_pane(self):
        """右ペインの作成（タブウィジェット）"""
        tab_widget = QTabWidget()

        # システム管理タブ
        system_tab = self._create_system_management_tab()
        tab_widget.addTab(system_tab, "システム管理")

        # 総合評価タブ
        evaluation_tab = self._create_evaluation_tab()
        tab_widget.addTab(evaluation_tab, "総合評価")

        return tab_widget

    def _create_system_management_tab(self):
        """システム管理タブの作成"""
        tab = QTabWidget()

        # 初期設定タブ
        settings_tab = self._create_settings_tab()
        tab.addTab(settings_tab, "初期設定")

        # データ入出力タブ
        io_tab = self._create_io_tab()
        tab.addTab(io_tab, "データ入出力")

        # システム情報タブ
        info_tab = self._create_info_tab()
        tab.addTab(info_tab, "システム情報")

        return tab

    def _create_settings_tab(self):
        """初期設定タブの作成"""
        tab = QWidget()
        layout = QHBoxLayout(tab)

        # グループリスト
        group_widget = QWidget()
        group_layout = QVBoxLayout(group_widget)
        group_layout.addWidget(QLabel("グループリスト"))
        self.settings_group_list = QListWidget()
        group_layout.addWidget(self.settings_group_list)

        group_buttons = QWidget()
        group_btn_layout = QVBoxLayout(group_buttons)
        self.add_group_btn = QPushButton("追加")
        self.edit_group_btn = QPushButton("編集")
        self.delete_group_btn = QPushButton("削除")
        group_btn_layout.addWidget(self.add_group_btn)
        group_btn_layout.addWidget(self.edit_group_btn)
        group_btn_layout.addWidget(self.delete_group_btn)
        group_layout.addWidget(group_buttons)
        
        layout.addWidget(group_widget)

        # カテゴリー管理
        category_widget = QWidget()
        category_layout = QVBoxLayout(category_widget)

        # 親カテゴリー
        category_layout.addWidget(QLabel("親カテゴリー"))
        self.category_list = QListWidget()
        category_layout.addWidget(self.category_list)

        category_buttons = QWidget()
        category_btn_layout = QVBoxLayout(category_buttons)
        self.add_category_btn = QPushButton("追加")
        self.edit_category_btn = QPushButton("編集")
        self.delete_category_btn = QPushButton("削除")
        category_btn_layout.addWidget(self.add_category_btn)
        category_btn_layout.addWidget(self.edit_category_btn)
        category_btn_layout.addWidget(self.delete_category_btn)
        category_layout.addWidget(category_buttons)

        # 子カテゴリー（スキル）
        category_layout.addWidget(QLabel("子カテゴリー（スキル）"))
        self.skill_list = QListWidget()
        category_layout.addWidget(self.skill_list)

        skill_buttons = QWidget()
        skill_btn_layout = QVBoxLayout(skill_buttons)
        self.add_skill_btn = QPushButton("追加")
        self.edit_skill_btn = QPushButton("編集")
        self.delete_skill_btn = QPushButton("削除")
        skill_btn_layout.addWidget(self.add_skill_btn)
        skill_btn_layout.addWidget(self.edit_skill_btn)
        skill_btn_layout.addWidget(self.delete_skill_btn)
        category_layout.addWidget(skill_buttons)

        layout.addWidget(category_widget)

        # 新規タブ追加ボタン
        new_tab_widget = QWidget()
        new_tab_layout = QVBoxLayout(new_tab_widget)
        self.add_new_tab_btn = QPushButton("新規タブ追加")
        self.add_new_tab_btn.clicked.connect(self.add_new_category_tab)
        new_tab_layout.addWidget(self.add_new_tab_btn)
        layout.addWidget(new_tab_widget)

        return tab

    def _create_io_tab(self):
        """データ入出力タブの作成"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # インポート
        import_group = QWidget()
        import_layout = QVBoxLayout(import_group)
        import_layout.addWidget(QLabel("データのインポート"))
        
        self.import_group_btn = QPushButton("グループリストのインポート")
        self.import_category_btn = QPushButton("カテゴリーリストのインポート")
        self.import_skill_btn = QPushButton("スキルレベルのインポート")
        
        import_layout.addWidget(self.import_group_btn)
        import_layout.addWidget(self.import_category_btn)
        import_layout.addWidget(self.import_skill_btn)
        
        layout.addWidget(import_group)

        # エクスポート
        export_group = QWidget()
        export_layout = QVBoxLayout(export_group)
        export_layout.addWidget(QLabel("データのエクスポート"))
        
        self.export_btn = QPushButton("PDF出力")
        export_layout.addWidget(self.export_btn)
        
        layout.addWidget(export_group)

        return tab

    def _create_info_tab(self):
        """システム情報タブの作成"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        info_text = """
        スキルマトリックス管理システム
        バージョン: 1.0.0
        最終更新日: 2025-02-07

        システム要件:
        - Python 3.8以上
        - PyQt6
        - SQLite3

        連携アプリケーション:
        - assignMeアプリ (開発予定)
        
        開発者: GingaDza
        Copyright © 2025 All rights reserved.
        """
        
        info_label = QLabel(info_text)
        info_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(info_label)
        
        return tab

    def _create_evaluation_tab(self):
        """総合評価タブの作成"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # チャート表示用のプレースホルダー
        chart_placeholder = QLabel("レーダーチャート表示エリア")
        chart_placeholder.setStyleSheet("background-color: #f0f0f0; min-height: 400px;")
        layout.addWidget(chart_placeholder)
        
        # 評価情報
        eval_info = QLabel("評価情報表示エリア")
        eval_info.setStyleSheet("background-color: #f0f0f0; min-height: 200px;")
        layout.addWidget(eval_info)
        
        return tab

    def load_data(self):
        """データの読み込み"""
        # グループの読み込み
        self.group_combo.clear()
        self.settings_group_list.clear()
        groups = self.db.get_all_groups()
        
        for group in groups:
            # メインのグループコンボボックス
            self.group_combo.addItem(group[1], group[0])
            # 設定タブのグループリスト
            item = QListWidgetItem(group[1])
            item.setData(Qt.ItemDataRole.UserRole, group[0])
            self.settings_group_list.addItem(item)

    def add_new_category_tab(self):
        """新規カテゴリータブの追加"""
        selected_items = self.category_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "カテゴリーを選択してください")
            return
            
        category = selected_items[0]
        tab = self._create_category_content_tab()
        # システム管理タブの左に追加
        self.tab_widget.insertTab(self.tab_widget.count() - 2, tab, category.text())

    def _create_category_content_tab(self):
        """カテゴリータブのコンテンツ作成"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # ユーザー情報
        user_info = QLabel("選択されたユーザー: なし")
        layout.addWidget(user_info)
        
        # スキルレベル設定
        skill_group = QWidget()
        skill_layout = QVBoxLayout(skill_group)
        skill_layout.addWidget(QLabel("スキルレベル設定"))
        
        # レベル設定用のプレースホルダー
        level_placeholder = QLabel("スキルレベル設定エリア")
        level_placeholder.setStyleSheet("background-color: #f0f0f0; min-height: 200px;")
        skill_layout.addWidget(level_placeholder)
        
        layout.addWidget(skill_group)
        
        # レーダーチャート
        chart_placeholder = QLabel("レーダーチャート表示エリア")
        chart_placeholder.setStyleSheet("background-color: #f0f0f0; min-height: 400px;")
        layout.addWidget(chart_placeholder)
        
        return tab

    def on_group_changed(self, index):
        """グループ選択時の処理"""
        if index >= 0:
            group_id = self.group_combo.itemData(index)
            self.load_users(group_id)

    def load_users(self, group_id):
        """ユーザーリストの読み込み"""
        self.user_list.clear()
        users = self.db.get_users_by_group(group_id)
        for user in users:
            item = QListWidgetItem(user[1])
            item.setData(Qt.ItemDataRole.UserRole, user[0])
            self.user_list.addItem(item)

    def on_user_selected(self):
        """ユーザー選択時の処理"""
        selected_items = self.user_list.selectedItems()
        if selected_items:
            self.update_user_skills(selected_items[0].data(Qt.ItemDataRole.UserRole))

    def update_user_skills(self, user_id):
        """ユーザーのスキルレベル表示を更新"""
        # 実装予定
        pass

    def add_user(self):
        """ユーザーの追加"""
        if self.group_combo.currentIndex() < 0:
            QMessageBox.warning(self, "警告", "グループを選択してください")
            return
            
        name, ok = QInputDialog.getText(self, "ユーザー追加", "ユーザー名を入力:")
        if ok and name:
            group_id = self.group_combo.currentData()
            # ユーザー追加の処理を実装予定
            self.load_users(group_id)

    def edit_user(self):
        """ユーザーの編集"""
        selected_items = self.user_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self,
# main_window.pyの続き (2025-02-07 14:09:41)

    def edit_user(self):
        """ユーザーの編集"""
        selected_items = self.user_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "ユーザーを選択してください")
            return
            
        current_name = selected_items[0].text()
        new_name, ok = QInputDialog.getText(
            self, "ユーザー編集", 
            "ユーザー名を入力:", 
            text=current_name
        )
        
        if ok and new_name:
            user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
            group_id = self.group_combo.currentData()
            # ユーザー編集の処理を実装予定
            self.load_users(group_id)

    def delete_user(self):
        """ユーザーの削除"""
        selected_items = self.user_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "ユーザーを選択してください")
            return
            
        reply = QMessageBox.question(
            self, "確認", 
            "選択したユーザーを削除しますか？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
            group_id = self.group_combo.currentData()
            # ユーザー削除の処理を実装予定
            self.load_users(group_id)

    def closeEvent(self, event):
        """アプリケーション終了時の処理"""
        self.logger.info("アプリケーションを終了します")
        event.accept()
