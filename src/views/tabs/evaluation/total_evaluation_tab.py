from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QScrollArea
)
from PyQt6.QtCore import Qt

# チャートモジュールの条件付きインポート
try:
    from PyQt6.QtCharts import QChart, QChartView, QPolarChart
    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False

class TotalEvaluationTab(QWidget):
    """総合評価タブ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = parent.db if parent else None
        self.setup_ui()

    def setup_ui(self):
        """UIの設定"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # フィルター部分
        filter_layout = QHBoxLayout()
        
        # グループフィルター
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self.update_chart)
        group_layout.addWidget(self.group_combo)
        filter_layout.addLayout(group_layout)

        # 表示方式フィルター
        view_layout = QHBoxLayout()
        view_layout.addWidget(QLabel("表示方式:"))
        self.view_combo = QComboBox()
        self.view_combo.addItems(["平均値", "最大値", "最小値"])
        self.view_combo.currentIndexChanged.connect(self.update_chart)
        view_layout.addWidget(self.view_combo)
        filter_layout.addLayout(view_layout)

        # 更新ボタン
        update_btn = QPushButton("更新")
        update_btn.clicked.connect(self.update_chart)
        filter_layout.addWidget(update_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # スクロールエリア（チャート表示用）
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.chart_layout = QVBoxLayout()
        scroll_widget.setLayout(self.chart_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        if CHARTS_AVAILABLE:
            self.initialize_charts()
        else:
            self.show_chart_error()

    def show_chart_error(self):
        """チャートが利用できない場合のエラーメッセージを表示"""
        error_label = QLabel(
            "チャート機能を使用するには PyQt6-Charts パッケージが必要です。\n"
            "インストールするには: pip install PyQt6-Charts"
        )
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("color: red;")
        self.chart_layout.addWidget(error_label)

    def initialize_charts(self):
        """レーダーチャートの初期化"""
        if not CHARTS_AVAILABLE:
            self.show_chart_error()
            return

        try:
            # メインチャート（全カテゴリー）
            main_chart = QPolarChart()
            main_chart.setTitle("全カテゴリー評価")
            main_chart_view = QChartView(main_chart)
            main_chart_view.setMinimumHeight(400)
            self.chart_layout.addWidget(main_chart_view)

            # カテゴリーごとのチャート
            categories = self.db.get_all_categories() if self.db else []
            for category in categories:
                chart = QPolarChart()
                chart.setTitle(f"{category[1]}の評価")  # category[1] は name
                chart_view = QChartView(chart)
                chart_view.setMinimumHeight(300)
                self.chart_layout.addWidget(chart_view)

        except Exception as e:
            error_label = QLabel(f"チャートの初期化中にエラーが発生しました: {str(e)}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.chart_layout.addWidget(error_label)

    def update_chart(self):
        """チャートの更新"""
        if not CHARTS_AVAILABLE:
            return

        try:
            group_id = self.group_combo.currentData()
            view_mode = self.view_combo.currentText()
            
            # TODO: データの取得と更新処理の実装
            self.initialize_charts()  # 仮の実装：チャートの再初期化
            
        except Exception as e:
            print(f"チャートの更新中にエラーが発生: {e}")
