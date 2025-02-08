"""設定ウィジェットの基本クラス"""
from ..base.base_widget import BaseWidget
from .group_manager import GroupManagerMixin
from .category_manager import CategoryManagerMixin
from .skill_manager import SkillManagerMixin

class SettingsWidgetBase(BaseWidget, GroupManagerMixin, CategoryManagerMixin, SkillManagerMixin):
    """設定ウィジェットの基本クラス"""

    def _on_group_selected(self, row: int):
        """グループ選択時のイベント"""
        try:
            group_item = self.category_group_combo.itemText(row)
            self.logger.info(f"グループ選択: {group_item}")
            
            # グループ選択を同期
            self._on_category_group_changed(row)
            
            # カテゴリー一覧を取得して最上位を選択
            categories = self._db_manager.get_categories_by_group(group_item)
            if categories:
                self.parent_list.setCurrentRow(0)  # 最上位のカテゴリーを選択
                self._on_parent_selected(0)  # カテゴリー選択時の処理を実行
                
                # スキル一覧を取得して最上位を選択
                skills = self._db_manager.get_skills_by_parent(categories[0])
                if skills:
                    self.child_list.setCurrentRow(0)  # 最上位のスキルを選択
                
        except Exception as e:
            self.logger.exception("グループ選択エラー")

    def _on_parent_selected(self, row: int):
        """カテゴリー選択時のイベント"""
        try:
            if row >= 0:
                parent_item = self.parent_list.item(row)
                if parent_item:
                    parent_name = parent_item.text()
                    group_name = self.category_group_combo.currentText()
                    self.logger.info(f"選択されたカテゴリー: {parent_name}, グループ: {group_name}")
                    
                    # スキル一覧を取得して最上位を選択
                    skills = self._db_manager.get_skills_by_parent(parent_name)
                    self.logger.info(f"カテゴリーのスキル: {skills}")
                    
                    self.child_list.clear()
                    self.child_list.addItems(skills)
                    
                    if skills:
                        self.child_list.setCurrentRow(0)  # 最上位のスキルを選択
                
        except Exception as e:
            self.logger.exception("親カテゴリー選択エラー")

    def _highlight_selected_items(self):
        """選択された項目をハイライト表示"""
        try:
            # グループのハイライト
            group_name = self.category_group_combo.currentText()
            if group_name:
                self._highlight_group(group_name)
            
            # カテゴリーのハイライト
            parent_item = self.parent_list.currentItem()
            if parent_item:
                self._highlight_parent(parent_item.text())
            
            # スキルのハイライト
            child_item = self.child_list.currentItem()
            if child_item:
                self._highlight_child(child_item.text())
                
        except Exception as e:
            self.logger.exception("ハイライト表示エラー")

    def _highlight_group(self, group_name: str):
        """グループをハイライト表示"""
        self.category_group_combo.setStyleSheet("""
            QComboBox {
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
                border-radius: 4px;
                padding: 4px;
            }
        """)

    def _highlight_parent(self, parent_name: str):
        """カテゴリーをハイライト表示"""
        for i in range(self.parent_list.count()):
            item = self.parent_list.item(i)
            if item.text() == parent_name:
                item.setBackground(self.palette().color(self.backgroundRole()).lighter(110))
            else:
                item.setBackground(self.palette().color(self.backgroundRole()))

    def _highlight_child(self, child_name: str):
        """スキルをハイライト表示"""
        for i in range(self.child_list.count()):
            item = self.child_list.item(i)
            if item.text() == child_name:
                item.setBackground(self.palette().color(self.backgroundRole()).lighter(110))
            else:
                item.setBackground(self.palette().color(self.backgroundRole()))

    def _connect_signals(self):
        """シグナルを接続"""
        super()._connect_signals()
        
        # 選択変更時のハイライト表示
        self.category_group_combo.currentIndexChanged.connect(lambda: self._highlight_selected_items())
        self.parent_list.currentItemChanged.connect(lambda: self._highlight_selected_items())
        self.child_list.currentItemChanged.connect(lambda: self._highlight_selected_items())