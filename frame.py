from PySide6 import QtGui
from PySide6.QtCore import QPoint, QRect, Signal
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QFrame


class Frame(QFrame):
    captured = Signal(QPoint, QPoint)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet("background: rgba(0, 0, 0, 0.00393)")
        self.begin = QPoint()
        self.end = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(0, 247, 247))
        pen.setStyle(QtGui.Qt.DashLine)
        pen.setDashPattern([5, 5, 5, 5])
        painter.setPen(pen)

        if not self.begin.isNull() and not self.end.isNull():
            rect = QRect(self.begin, self.end)
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.captured.emit(self.begin, self.end)
        self.begin = QPoint()
        self.end = QPoint()
        self.update()
