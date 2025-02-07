# ... [import文は変更なし] ...

class MainWindow(QMainWindow):
    # ... [前半部分は変更なし] ...

    def load_groups(self):
        """グループリストの読み込み"""
        self.group_list.clear()
        groups = self.db.get_all_groups()
        for group in groups:
            item = QListWidgetItem(str(group[1]))
            item.setData(Qt.UserRole, group[0])  # IDを保存
            self.group_list.addItem(item)

    def on_group_selected(self):
        """グループ選択時の処理"""
        selected = self.group_list.selectedItems()
        if selected:
            group_id = selected[0].data(Qt.UserRole)
            self.load_categories(group_id)

    def load_categories(self, group_id):
        """カテゴリーリストの読み込み"""
        self.category_list.clear()
        self.skill_list.clear()
        categories = self.db.get_categories_by_group(group_id)
        for category in categories:
            item = QListWidgetItem(str(category[1]))
            item.setData(Qt.UserRole, category[0])  # IDを保存
            self.category_list.addItem(item)

    def on_category_selected(self):
        """カテゴリー選択時の処理"""
        selected = self.category_list.selectedItems()
        if selected:
            category_id = selected[0].data(Qt.UserRole)
            self.load_skills(category_id)

    def load_skills(self, category_id):
        """スキルリストの読み込み"""
        self.skill_list.clear()
        skills = self.db.get_skills_by_category(category_id)
        for skill in skills:
            item = QListWidgetItem(str(skill[1]))
            item.setData(Qt.UserRole, skill[0])  # IDを保存
            self.skill_list.addItem(item)

    # ... [その他のメソッドは変更なし] ...
