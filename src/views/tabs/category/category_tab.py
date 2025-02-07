from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTabWidget,
    QPushButton,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtChart import QChart, QChartView, QPolarChart
from ...components.categories.category_tree_widget import CategoryTreeWidget

class CategoryTab(QWidget):
    """カテゴリーベースのスキル管理タブ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """UIコンポーネントの設定"""
        layout = QHBoxLayout()
        self.setLayout(layout)

        # 左側：カテゴリーツリー（1/3）
        tree_container = QWidget()
        tree_layout = QVBoxLayout()
        tree_container.setLayout(tree_layout)

        self.category_tree = CategoryTreeWidget()
        tree_layout.addWidget(QLabel("カテゴリー"))
        tree_layout.addWidget(self.category_tree)

        # 右側：スキル詳細とレーダーチャート（2/3）
        content_container = QWidget()
        content_layout = QVBoxLayout()
        content_container.setLayout(content_layout)

        # レーダーチャート
        self.chart = QPolarChart()
        self.chart.setTitle("スキルレーダーチャート")
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # スキル一覧とレベル入力
        self.skill_tab_widget = QTabWidget()
        
        content_layout.addWidget(self.chart_view, stretch=1)
        content_layout.addWidget(self.skill_tab_widget, stretch=2)

        # レイアウトの比率設定（1:2）
        layout.addWidget(tree_container, stretch=1)
        layout.addWidget(content_container, stretch=2)

    def setup_connections(self):
        """シグナル/スロット接続"""
        self.category_tree.currentItemChanged.connect(self.on_category_selected)

    def on_category_selected(self, current, previous):
        """カテゴリー選択時の処理"""
        if current:
            category_id = current.data(0, Qt.ItemDataRole.UserRole)
            self.load_category_skills(category_id)
            self.update_radar_chart(category_id)

    def load_category_skills(self, category_id):
        """カテゴリーに属するスキルの読み込み"""
        # TODO: スキルデータの読み込みと表示
        pass

    def update_radar_chart(self, category_id):
        """レーダーチャートの更新"""
        # TODO: チャートデータの更新
        self.chart.removeAllSeries()
        # TODO: データに基づいてシリーズを追加
        pass

    def add_skill_tab(self, category_id, skill_data):
        """スキルタブの追加"""
        # TODO: スキルごとのタブを追加
        pass

    def remove_skill_tab(self, skill_id):
        """スキルタブの削除"""
        # TODO: 指定されたスキルのタブを削除
        pass

    def refresh(self):
        """表示の更新"""
        self.category_tree.refresh()
        # TODO: 現在選択中のカテゴリーの再読み込み
