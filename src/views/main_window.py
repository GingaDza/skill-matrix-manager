# ... [前のインポート文は同じ] ...

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

        # 初期データの読み込み
        self.load_data()

    def _create_right_pane(self):
        """右ペインの作成（タブウィジェット）"""
        tab_widget = QTabWidget()
        tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        tab_widget.setMovable(True)  # タブの移動を許可

        # システム管理タブ（デフォルト）
        system_tab = self._create_system_management_tab()
        tab_widget.addTab(system_tab, "システム管理")

        # 総合評価タブ
        evaluation_tab = self._create_evaluation_tab()
        tab_widget.addTab(evaluation_tab, "総合評価")

        return tab_widget

    # ... [その他のメソッドは同じ] ...

    def add_new_category_tab(self):
        """新規カテゴリータブの追加"""
        selected_items = self.category_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "カテゴリーを選択してください")
            return
            
        category = selected_items[0]
        tab = self._create_category_content_tab(category.text())

        # システム管理タブの左に追加（総合評価タブの左）
        insert_index = self.get_category_tab_insert_position()
        self.tab_widget.insertTab(insert_index, tab, category.text())
        self.tab_widget.setCurrentIndex(insert_index)  # 新しいタブを選択

    def get_category_tab_insert_position(self):
        """カテゴリータブの挿入位置を取得"""
        total_tabs = self.tab_widget.count()
        # システム管理タブと総合評価タブの前に挿入
        return max(0, total_tabs - 2)

    def _create_category_content_tab(self, category_name):
        """カテゴリータブのコンテンツ作成"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # ヘッダー（グループとユーザー情報）
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        group_label = QLabel(f"グループ: {self.group_combo.currentText()}")
        header_layout.addWidget(group_label)
        
        user_label = QLabel("選択ユーザー: なし")
        if self.user_list.selectedItems():
            user_label.setText(f"選択ユーザー: {self.user_list.selectedItems()[0].text()}")
        header_layout.addWidget(user_label)
        
        layout.addWidget(header)
        
        # スキル一覧とレベル設定
        skills_widget = QWidget()
        skills_layout = QVBoxLayout(skills_widget)
        skills_layout.addWidget(QLabel(f"{category_name} スキル一覧"))
        
        # スキルレベル設定グリッド
        self.skill_levels = {}  # スキルIDとスピンボックスの辞書
        for skill in self.get_skills_for_category(category_name):
            skill_row = QWidget()
            skill_layout = QHBoxLayout(skill_row)
            
            skill_label = QLabel(skill['name'])
            skill_layout.addWidget(skill_label)
            
            level_spin = QSpinBox()
            level_spin.setRange(1, 5)
            level_spin.setValue(1)
            level_spin.valueChanged.connect(
                lambda v, s=skill['id']: self.on_skill_level_changed(s, v)
            )
            self.skill_levels[skill['id']] = level_spin
            skill_layout.addWidget(level_spin)
            
            skills_layout.addWidget(skill_row)
        
        layout.addWidget(skills_widget)
        
        # レーダーチャート
        chart_widget = QWidget()
        chart_layout = QVBoxLayout(chart_widget)
        chart_layout.addWidget(QLabel("スキルレーダーチャート"))
        
        chart_placeholder = QLabel("レーダーチャート表示エリア")
        chart_placeholder.setStyleSheet(
            "background-color: #f0f0f0; min-height: 400px;"
        )
        chart_layout.addWidget(chart_placeholder)
        
        layout.addWidget(chart_widget)
        
        return tab

    def get_skills_for_category(self, category_name):
        """カテゴリーに属するスキル一覧を取得"""
        # TODO: データベースから実際のスキル一覧を取得
        return [
            {'id': 1, 'name': 'スキル1'},
            {'id': 2, 'name': 'スキル2'},
            {'id': 3, 'name': 'スキル3'},
        ]

    def on_skill_level_changed(self, skill_id, value):
        """スキルレベル変更時の処理"""
        if self.user_list.selectedItems():
            user_id = self.user_list.selectedItems()[0].data(Qt.ItemDataRole.UserRole)
            self.db.update_skill_level(user_id, skill_id, value)
            self.update_charts()

