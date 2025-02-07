"""レーダーチャートウィジェット"""
import logging
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt

class RadarChartWidget(QWidget):
    """レーダーチャートウィジェット"""
    
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
            
            # 中心点と半径の計算
            center_x = self.width() / 2
            center_y = self.height() / 2
            radius = min(center_x, center_y) * 0.8
            
            # 背景の描画
            self._draw_background(painter, center_x, center_y, radius)
            
            # データの描画
            if self._data:
                self._draw_data(painter, center_x, center_y, radius)
                
        except Exception as e:
            self.logger.exception("レーダーチャート描画エラー")

    def _draw_background(self, painter: QPainter, cx: float, cy: float, radius: float):
        """背景の描画"""
        try:
            pen = QPen(Qt.GlobalColor.gray)
            pen.setWidth(1)
            painter.setPen(pen)
            
            # レベル円の描画
            for i in range(1, 6):  # 5段階
                r = radius * i / 5
                painter.drawEllipse(
                    int(cx - r),
                    int(cy - r),
                    int(r * 2),
                    int(r * 2)
                )
            
            # 軸の描画
            if self._data:
                n = len(self._data)
                for i in range(n):
                    angle = i * 2 * math.pi / n
                    x = cx + radius * math.cos(angle)
                    y = cy + radius * math.sin(angle)
                    painter.drawLine(
                        int(cx),
                        int(cy),
                        int(x),
                        int(y)
                    )
                    
        except Exception as e:
            self.logger.exception("背景描画エラー")

    def _draw_data(self, painter: QPainter, cx: float, cy: float, radius: float):
        """データの描画"""
        try:
            # データポイントの計算
            points = []
            values = list(self._data.values())
            n = len(values)
            
            for i, value in enumerate(values):
                angle = i * 2 * math.pi / n
                r = radius * value / 5
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                points.append((int(x), int(y)))
            
            # データ線の描画
            pen = QPen(QColor(0, 120, 215))
            pen.setWidth(2)
            painter.setPen(pen)
            
            for i in range(n):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % n]
                painter.drawLine(x1, y1, x2, y2)
                
        except Exception as e:
            self.logger.exception("データ描画エラー")
