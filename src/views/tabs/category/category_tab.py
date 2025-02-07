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

try:
    from PyQt6.QtChart import QChart, QChartView, QPolarChart
    CHART_AVAILABLE = True
except ImportError:
    CHART_AVAILABLE = False

from ...components.categories.category_tree_widget import CategoryTreeWidget

class CategoryTab(QWidget):
    """カテゴリーベースのスキル管理タブ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = parent.db if parent else None
        self.setup_ui()

    def setup_ui(self):
        """UIコンポーネントの設定"""
        layout = QHBoxLayout()
        self.setLayout(layout)

        # 左側：カテゴリーツリー（1/3）
        tree_container = QWidget()
        tree_layout = QVBoxLayout()
        tree_container.setLayout(tree_layout)

        self.category_tree = CategoryTreeWidget(self)
        tree_layout.addWidget(QLabel("カテゴリー"))
        tree_layout.addWidget(self.category_tree)

        # 右側：スキル詳細とレーダーチャート（2/3）
        content_container = QWidget()
        content_layout = QVBoxLayout()
        content_container.setLayout(content_layout)

        # レーダーチャート
        if CHART_AVAILABLE:
            self.chart = QPolarChart()
            self.chart.setTitle("スキルレーダーチャート")
            self.chart_view = QChartView(self.chart)
            content_layout.addWidget(self.chart_view, stretch=1)
        else:
            chart_label = QLabel("※ チャート機能を利用するには PyQt6-Charts をインストールしてください")
            chart_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            content_layout.addWidget(chart_label, stretch=1)

        # スキル一覧とレベル入力
        self.skill_tab_widget = QTabWidget()
        content_layout.addWidget(self.skill_tab_widget, stretch=2)

        # レイアウトの比率設定（1:2）
        layout.addWidget(tree_container, stretch=1)
        layout.addWidget(content_container, stretch=2)

    def on_category_selected(self, category_id):
        """カテゴリー選択時の処理"""
        if category_id:
            self.load_category_skills(category_id)

    def load_category_skills(self, category_id):
        """カテゴリーに属するスキルの読み込み"""
        # TODO: スキルデータの読み込みと表示
        pass

    def refresh(self):
        """表示の更新"""
        self.category_tree.refresh()
