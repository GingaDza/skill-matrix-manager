"""レーダーチャートモジュール"""
import logging
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
import math

class RadarChart(QWidget):
    """レーダーチャートクラス"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._data = {}
        self.setMinimumSize(300, 300)

    def update_data(self, data: dict):
        """データの更新"""
        self._data = data
        self.update()

    def paintEvent(self, event):
        """描画イベント"""
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 中心点
            center_x = self.width() / 2
            center_y = self.height() / 2
            
            # 半径
            radius = min(center_x, center_y) * 0.8
            
            # 軸の描画
            self._draw_axes(painter, center_x, center_y, radius)
            
            # データの描画
            if self._data:
                self._draw_data(painter, center_x, center_y, radius)
                
        except Exception as e:
            self.logger.exception("レーダーチャート描画エラー")

    def _draw_axes(self, painter: QPainter, cx: float, cy: float, radius: float):
        """軸の描画"""
        try:
            # ペンの設定
            pen = QPen(Qt.GlobalColor.gray)
            pen.setWidth(1)
            painter.setPen(pen)
            
            # 軸の数
            num_axes = 5
            
            for i in range(num_axes):
                angle = i * 2 * math.pi / num_axes
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                painter.drawLine(int(cx), int(cy), int(x), int(y))
                
        except Exception as e:
            self.logger.exception("軸描画エラー")

    def _draw_data(self, painter: QPainter, cx: float, cy: float, radius: float):
        """データの描画"""
        try:
            # ペンの設定
            pen = QPen(QColor(0, 120, 215))
            pen.setWidth(2)
            painter.setPen(pen)
            
            # データポイントの描画
            points = []
            num_points = len(self._data)
            
            for i, value in enumerate(self._data.values()):
                angle = i * 2 * math.pi / num_points
                r = radius * value / 5  # 5段階評価を前提
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                points.append((int(x), int(y)))
            
            # ポリゴンの描画
            for i in range(len(points)):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % len(points)]
                painter.drawLine(x1, y1, x2, y2)
                
        except Exception as e:
            self.logger.exception("データ描画エラー")

