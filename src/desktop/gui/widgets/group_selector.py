# src/desktop/gui/widgets/group_selector.py
"""
Group selector widget implementation
Created: 2025-01-31 21:57:46
Author: GingaDza
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QMenu, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction

class GroupSelector(QWidget):
    # グループ選択変更シグナル
    group_changed = Signal(str)  # group_id
    
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()
        self.setup_signals()
    
    def setup_ui(self):
        """UIの初期設定"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # グループ選択コンボボックス
        self.combo = QComboBox()
        self.combo.setMinimumWidth(200)
        layout.addWidget(self.combo)
        
        # グループ管理ボタン
        self.manage_btn = QPushButton("管理")
        self.manage_btn.setMaximumWidth(60)
        layout.addWidget(self.manage_btn)
        
        # 管理メニュー
        self.menu = QMenu(self)
        
        # グループ追加アクション
        self.add_action = QAction("新規グループ", self)
        self.add_action.triggered.connect(self.add_group)
        self.menu.addAction(self.add_action)
        
        # グループ編集アクション
        self.edit_action = QAction("グループ編集", self)
        self.edit_action.triggered.connect(self.edit_group)
        self.menu.addAction(self.edit_action)
        
        # グループ削除アクション
        self.delete_action = QAction("グループ削除", self)
        self.delete_action.triggered.connect(self.delete_group)
        self.menu.addAction(self.delete_action)
        
        # ボタンにメニューを設定
        self.manage_btn.setMenu(self.menu)
    
    def setup_signals(self):
        """シグナル/スロット接続"""
        self.combo.currentIndexChanged.connect(self.on_selection_changed)
        self.data_manager.groups_changed.connect(self.update_groups)
        
        # 初期表示
        self.update_groups()
    
# src/desktop/gui/widgets/group_selector.py の update_groups メソッドを修正

# src/desktop/gui/widgets/group_selector.py
    def update_groups(self):
        """グループ一覧の更新"""
        current_id = self.combo.currentData()
        
        self.combo.clear()
        self.combo.addItem("すべて", None)
        
        # グループの一覧を取得して表示（カテゴリーではなく、グループを表示）
        for group in self.data_manager.get_all_groups():
            self.combo.addItem(group.name, group.id)
        
        # 選択状態の復元
        if current_id:
            index = self.combo.findData(current_id)
            if index >= 0:
                self.combo.setCurrentIndex(index)
        
        # アクションの有効/無効を設定
        has_selection = self.get_selected_group_id() is not None
        self.edit_action.setEnabled(has_selection)
        self.delete_action.setEnabled(has_selection)
    
    def get_selected_group_id(self) -> str:
        """選択中のグループIDを取得"""
        return self.combo.currentData()
    
    def on_selection_changed(self):
        """グループ選択時の処理"""
        group_id = self.get_selected_group_id()
        self.group_changed.emit(group_id)
        
        # アクションの有効/無効を設定
        has_selection = group_id is not None
        self.edit_action.setEnabled(has_selection)
        self.delete_action.setEnabled(has_selection)
    
    def add_group(self):
        """新規グループの追加"""
        from ..dialogs.group_dialog import GroupDialog
        dialog = GroupDialog(self.data_manager, self)
        dialog.exec()
    
    def edit_group(self):
        """選択中のグループを編集"""
        group_id = self.get_selected_group_id()
        if not group_id:
            return
        
        group = self.data_manager.groups.get(group_id)
        if group:
            from ..dialogs.group_dialog import GroupDialog
            dialog = GroupDialog(self.data_manager, self, group)
            dialog.exec()
    
    def delete_group(self):
        """選択中のグループを削除"""
        group_id = self.get_selected_group_id()
        if not group_id:
            return
        
        group = self.data_manager.groups.get(group_id)
        if group:
            # グループにメンバーがいる場合は確認
            if group.members:
                reply = QMessageBox.question(
                    self,
                    "グループ削除",
                    f"グループ「{group.name}」には{len(group.members)}名のメンバーがいます。\n"
                    "グループを削除すると、メンバーはグループなしになります。\n"
                    "削除してもよろしいですか？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
            else:
                reply = QMessageBox.question(
                    self,
                    "グループ削除",
                    f"グループ「{group.name}」を削除してもよろしいですか？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
            
            if reply == QMessageBox.Yes:
                self.data_manager.delete_group(group_id)