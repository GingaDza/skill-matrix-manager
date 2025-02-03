from PyQt6.QtWidgets import (
    QVBoxLayout, QPushButton, QHBoxLayout,
    QListWidget, QLabel
)

class CategoryUIManager:
    def __init__(self, parent, debug_logger):
        self.parent = parent
        self.debug_logger = debug_logger
        self.setup_components()
        
    def setup_components(self):
        self.debug_logger.log_method_call("setup_components")
        # 親カテゴリー関連
        self.parent_list = QListWidget()
        self.add_parent_btn = QPushButton("追加")
        self.edit_parent_btn = QPushButton("編集")
        self.delete_parent_btn = QPushButton("削除")
        
        # 子カテゴリー関連
        self.child_list = QListWidget()
        self.add_child_btn = QPushButton("追加")
        self.edit_child_btn = QPushButton("編集")
        self.delete_child_btn = QPushButton("削除")
        
    def setup_ui(self):
        self.debug_logger.log_method_call("setup_ui")
        layout = QVBoxLayout()
        
        # 親カテゴリーセクション
        parent_section = QVBoxLayout()
        parent_section.addWidget(QLabel("親カテゴリー"))
        parent_section.addWidget(self.parent_list)
        
        parent_buttons = QHBoxLayout()
        for btn in [self.add_parent_btn, self.edit_parent_btn, self.delete_parent_btn]:
            parent_buttons.addWidget(btn)
        parent_section.addLayout(parent_buttons)
        
        # 子カテゴリーセクション
        child_section = QVBoxLayout()
        child_section.addWidget(QLabel("子カテゴリー（スキル）"))
        child_section.addWidget(self.child_list)
        
        child_buttons = QHBoxLayout()
        for btn in [self.add_child_btn, self.edit_child_btn, self.delete_child_btn]:
            child_buttons.addWidget(btn)
        child_section.addLayout(child_buttons)
        
        # メインレイアウトに追加
        layout.addLayout(parent_section)
        layout.addLayout(child_section)
        
        self.parent.setLayout(layout)