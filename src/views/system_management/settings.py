"""初期設定ウィジェット"""
from .settings_base import SettingsWidgetBase
from .group_manager import GroupManagerMixin
from .category_manager import CategoryManagerMixin
from .skill_manager import SkillManagerMixin

class SettingsWidget(SettingsWidgetBase, GroupManagerMixin, CategoryManagerMixin, SkillManagerMixin):
    """初期設定タブのウィジェット"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_ui()
        self._connect_signals()
        self._load_data()

    def _init_ui(self):
        """UIの初期化"""
        # グループリスト
        group_box = self._create_group_list()
        self.main_layout.addWidget(group_box)
        
        # カテゴリーリスト
        category_box = self._create_category_lists()
        self.main_layout.addWidget(category_box)
        
        self.logger.info("UI initialized")

    def _connect_signals(self):
        """シグナルとスロットの接続"""
        # グループ操作
        self.add_group_btn.clicked.connect(self._on_add_group)
        self.edit_group_btn.clicked.connect(self._on_edit_group)
        self.delete_group_btn.clicked.connect(self._on_delete_group)
        
        # カテゴリー操作
        self.add_category_btn.clicked.connect(self._on_add_category)
        self.edit_category_btn.clicked.connect(self._on_edit_category)
        self.delete_category_btn.clicked.connect(self._on_delete_category)
        
        # スキル操作
        self.add_skill_btn.clicked.connect(self._on_add_skill)
        self.edit_skill_btn.clicked.connect(self._on_edit_skill)
        self.delete_skill_btn.clicked.connect(self._on_delete_skill)
        
        # タブ操作
        self.new_tab_btn.clicked.connect(self._on_add_new_tab)
        
        # リスト選択
        self.parent_list.currentRowChanged.connect(self._on_parent_selected)
        self.category_group_combo.currentTextChanged.connect(self._on_category_group_changed)
        self.group_list.currentRowChanged.connect(self._on_group_selected)
        
        self.logger.info("Signals connected")

    def _on_group_selected(self, row: int):
        """グループ選択時のイベント"""
        if row >= 0:
            selected_group = self.group_list.item(row).text()
            self.logger.info(f"グループ選択: {selected_group}")
            self._sync_group_selections(selected_group)

    def _on_add_new_tab(self):
        """新規タブ追加"""
        try:
            current_item = self.parent_list.currentItem()
            if not current_item:
                raise Exception("タブとして追加する親カテゴリーを選択してください。")
                
            category_name = current_item.text()
            group_name = self.category_group_combo.currentText()
            
            # TODO: メインウィンドウへのタブ追加通知を実装
            self.logger.info(f"新規タブ追加: {category_name} (グループ: {group_name})")
            QMessageBox.information(
                self,
                "成功",
                f"カテゴリー「{category_name}」をタブとして追加しました。"
            )
            
        except Exception as e:
            self.logger.exception("タブ追加エラー")
            QMessageBox.critical(
                self,
                "エラー",
                str(e)
            )
