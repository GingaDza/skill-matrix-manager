# src/desktop/gui/widgets/user_list.py
"""
User list widget implementation
Created: 2025-01-31 14:28:24
Author: GingaDza
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton,
    QLabel, QMenu, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction

class UserList(QWidget):
    # ユーザー選択シグナル
    user_selected = Signal(str)  # user_id
    
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_group_id = None
        self.setup_ui()
        self.setup_signals()
        self.setup_context_menu()
    
    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # ヘッダー部分
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # タイトル
        self.title_label = QLabel("ユーザー一覧")
        self.title_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(self.title_label)
        
        # スペーサー
        header_layout.addStretch()
        
        # ユーザー追加ボタン
        self.add_user_btn = QPushButton("ユーザー追加")
        self.add_user_btn.setMaximumWidth(100)
        header_layout.addWidget(self.add_user_btn)
        
        layout.addWidget(header)
        
        # ユーザーリスト
        self.list = QListWidget()
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        layout.addWidget(self.list)
        
        # ステータス表示
        self.status_label = QLabel()
        layout.addWidget(self.status_label)
    
    def setup_signals(self):
        """シグナル/スロット接続"""
        self.add_user_btn.clicked.connect(self.add_user)
        self.list.itemSelectionChanged.connect(self.on_selection_changed)
        self.list.customContextMenuRequested.connect(self.show_context_menu)
        self.data_manager.users_changed.connect(self.update_users)
        self.data_manager.groups_changed.connect(self.update_group_info)
        
        # 初期表示
        self.update_users()
    
    def setup_context_menu(self):
        """コンテキストメニューの設定"""
        self.context_menu = QMenu(self)
        
        # ユーザー編集アクション
        self.edit_action = QAction("編集", self)
        self.edit_action.triggered.connect(self.edit_user)
        self.context_menu.addAction(self.edit_action)
        
        # グループ移動サブメニュー
        self.move_menu = QMenu("グループ移動", self)
        self.context_menu.addMenu(self.move_menu)
        
        # 削除アクション
        self.delete_action = QAction("削除", self)
        self.delete_action.triggered.connect(self.delete_user)
        self.context_menu.addAction(self.delete_action)
    
    def update_users(self, group_id: str = None):
        """ユーザー一覧の更新"""
        self.current_group_id = group_id
        self.list.clear()
        
        users = self.data_manager.get_group_users(group_id)
        for user in users:
            item = QListWidgetItem(user.name)
            item.setData(Qt.UserRole, user.id)
            item.setToolTip(f"メール: {user.email}")
            self.list.addItem(item)
        
        # ステータス更新
        self.update_status()
    
    def update_group_info(self):
        """グループ情報の更新"""
        if self.current_group_id:
            group = self.data_manager.groups.get(self.current_group_id)
            if group:
                self.title_label.setText(f"ユーザー一覧 - {group.name}")
            else:
                self.title_label.setText("ユーザー一覧")
                self.current_group_id = None
                self.update_users()
        
        # 移動メニューの更新
        self.update_move_menu()
    
    def update_move_menu(self):
        """グループ移動メニューの更新"""
        self.move_menu.clear()
        
        # グループなしオプション
        action = QAction("グループなし", self)
        action.setData(None)
        action.triggered.connect(lambda: self.move_user_to_group(None))
        self.move_menu.addAction(action)
        
        if self.data_manager.groups:
            self.move_menu.addSeparator()
            
            # グループ一覧
            for group in self.data_manager.groups.values():
                if group.id != self.current_group_id:
                    action = QAction(group.name, self)
                    action.setData(group.id)
                    action.triggered.connect(
                        lambda checked, g=group.id: self.move_user_to_group(g)
                    )
                    self.move_menu.addAction(action)
    
    def update_status(self):
        """ステータス表示の更新"""
        count = self.list.count()
        self.status_label.setText(f"ユーザー数: {count}")
    
    def add_user(self):
        """新規ユーザーの追加"""
        from ..dialogs.user_dialog import UserDialog
        dialog = UserDialog(self.data_manager, self)
        if dialog.exec():
            self.update_users(self.current_group_id)
    
    def edit_user(self):
        """選択中のユーザーを編集"""
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        
        user = self.data_manager.users.get(user_id)
        if user:
            from ..dialogs.user_dialog import UserDialog
            dialog = UserDialog(self.data_manager, self, user)
            if dialog.exec():
                self.update_users(self.current_group_id)
    
    def delete_user(self):
        """選択中のユーザーを削除"""
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        
        user = self.data_manager.users.get(user_id)
        if user:
            reply = QMessageBox.question(
                self,
                "ユーザー削除",
                f"ユーザー「{user.name}」を削除してもよろしいですか？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.data_manager.delete_user(user_id)
                self.update_users(self.current_group_id)
    
    def move_user_to_group(self, group_id: str):
        """ユーザーを指定のグループに移動"""
        user_id = self.get_selected_user_id()
        if not user_id:
            return
        
        try:
            self.data_manager.update_user_group(user_id, group_id)
            self.update_users(self.current_group_id)
        except ValueError as e:
            QMessageBox.warning(self, "エラー", str(e))
    
    def get_selected_user_id(self) -> str:
        """選択中のユーザーIDを取得"""
        items = self.list.selectedItems()
        if items:
            return items[0].data(Qt.UserRole)
        return None
    
    def on_selection_changed(self):
        """ユーザー選択時の処理"""
        user_id = self.get_selected_user_id()
        self.user_selected.emit(user_id)
        
        # コンテキストメニューの有効/無効を設定
        has_selection = bool(user_id)
        self.edit_action.setEnabled(has_selection)
        self.move_menu.setEnabled(has_selection)
        self.delete_action.setEnabled(has_selection)
    
    def show_context_menu(self, pos):
        """コンテキストメニューの表示"""
        if self.get_selected_user_id():
            self.context_menu.exec(self.list.mapToGlobal(pos))