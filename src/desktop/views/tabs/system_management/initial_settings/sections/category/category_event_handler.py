from PyQt6.QtWidgets import QDialog, QMessageBox
from views.dialogs.input_dialog import InputDialog  # インポートパスを修正

class CategoryEventHandler:
    def __init__(self, parent, data_manager, ui_manager, debug_logger):
        self.parent = parent
        self.data_manager = data_manager
        self.ui_manager = ui_manager
        self.debug_logger = debug_logger
        
    def setup_connections(self):
        self.debug_logger.log_method_call("setup_connections")
        
        # 親カテゴリーのイベント
        self.ui_manager.add_parent_btn.clicked.connect(self.handle_add_parent)
        self.ui_manager.edit_parent_btn.clicked.connect(self.handle_edit_parent)
        self.ui_manager.delete_parent_btn.clicked.connect(self.handle_delete_parent)
        self.ui_manager.parent_list.itemSelectionChanged.connect(
            self.handle_parent_selection_changed)
        
        # 子カテゴリーのイベント
        self.ui_manager.add_child_btn.clicked.connect(self.handle_add_child)
        self.ui_manager.edit_child_btn.clicked.connect(self.handle_edit_child)
        self.ui_manager.delete_child_btn.clicked.connect(self.handle_delete_child)
        self.ui_manager.child_list.itemSelectionChanged.connect(
            self.handle_child_selection_changed)

    def handle_add_parent(self):
        self.debug_logger.log_method_call("handle_add_parent")
        dialog = InputDialog("親カテゴリー追加", "カテゴリー名:", parent=self.parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.get_input().strip()
            if name:
                self.data_manager.add_parent_category(name)
                self.ui_manager.update_parent_list()

    def handle_edit_parent(self):
        self.debug_logger.log_method_call("handle_edit_parent")
        current_item = self.ui_manager.parent_list.currentItem()
        if current_item:
            old_name = current_item.text()
            dialog = InputDialog("親カテゴリー編集", "新しいカテゴリー名:", old_name, self.parent)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_name = dialog.get_input().strip()
                if new_name and new_name != old_name:
                    self.data_manager.edit_parent_category(old_name, new_name)
                    self.ui_manager.update_parent_list()

    def handle_delete_parent(self):
        self.debug_logger.log_method_call("handle_delete_parent")
        current_item = self.ui_manager.parent_list.currentItem()
        if current_item:
            name = current_item.text()
            if self.show_confirmation(f"親カテゴリー '{name}' を削除しますか？"):
                self.data_manager.delete_parent_category(name)
                self.ui_manager.update_parent_list()
                self.ui_manager.clear_child_list()

    def show_confirmation(self, message):
        return QMessageBox.question(
            self.parent, "確認", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes