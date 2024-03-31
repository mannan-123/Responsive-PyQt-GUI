from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEasingCurve, QPoint
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty


class PyToggle (QCheckBox):
    def __init__(
        self,
        width = 60,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#00BCff",
        animation_curve = QEasingCurve.OutBounce
    ):
        QCheckBox.__init__(self)
        # SET DEFALT PARAMETERS
        self.setFixedSize(width, 28)
        self.setCursor(Qt. PointingHandCursor)

        # COLORS
        self._bg_color= bg_color
        self._circle_color = circle_color
        self._active_color= active_color

        # CREATE ANIMATION
        self._circle_position = 15
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500) # Time in milissecon
        
        # CONNECT STATE CHANGE
        self.stateChanged.connect(self.start_animation)

    # Define a custom signal
    styleChanged = pyqtSignal(bool)

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position
    
    @circle_position.setter
    def circle_position(self, value):
        self._circle_position = value
        self.update()

    def debug(self, value):
        print("State: ", self.isChecked())

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def start_animation(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 15)
        else:
            self.animation.setEndValue(16)
        self.animation.start()
        
        self.styleChanged.emit(value)
        # print("State: ", self.isChecked())

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        react = QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0,0,react.width(), self.height(), self.height()/2, self.height()/2)
            p.setBrush(QColor(self._circle_color))
            # p.drawEllipse(self._circle_position, 3, 22, 22)
            center_point = QPointF(self._circle_position, self.height() / 2)
            p.drawEllipse(center_point, 11, 11)

        else:
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0,0,react.width(), self.height(), self.height()/2, self.height()/2)
            p.setBrush(QColor(self._circle_color))
            # p.drawEllipse(self._circle_position, 3, 22, 22)
            center_point = QPointF(self._circle_position, self.height() / 2)
            p.drawEllipse(center_point, 11, 11)
        p.end()
