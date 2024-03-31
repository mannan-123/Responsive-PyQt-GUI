from PyQt5.QtWidgets import (
    QApplication, QFrame, QMainWindow, QWidget, QLabel, QHBoxLayout
)
from PyQt5 import QtGui, QtCore  # Add QtCore to your imports
import sys
from PyQt5.uic import loadUi
from icons.icons import *
from PyQt5.QtCore import Qt, QPoint
from toggle import PyToggle
from stylesheet import Stylesheet

# hanldes the window maximize and restore
GLOBAL_STATE = 0

class MainWindow(QMainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()

        # Here we imported the QT Designer UI file
        loadUi("GUI.ui", self)

        # set light and dark
        self.lightDarkModeUI()

        # remove stysheets
        self.remove_stylesheets()

        self.setStyleSheet(Stylesheet.lightMode())  # Set the light theme by default

        # showing the gui and selected page widget
        self.show()
        self.stackedWidget.setCurrentWidget(self.page)

        # change the tabs using the buttons
        self.eduButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page))
        self.selfCheckButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.faqButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))
        self.aboutButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_4))
        self.settingButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_5))

        # remove the title bar
        self.removeTitleBar()

        # close the window
        self.closeButton.clicked.connect(lambda: self.close())
        # minize the window
        self.minButton.clicked.connect(lambda: self.showMinimized())
        # maximize the window
        self.maxMinButton.clicked.connect(self.maximizeRestore)

        # make the window draggable
        self.draggable = True
        self.drag_position = QPoint()

        # restore and maximize from the title bar
        self.topFrame.mouseDoubleClickEvent = self.dobleClickMaximizeRestore

        # self.get_all_styles()

    # def get_all_styles(self):
    #     # Get the existing stylesheet from all child widgets
    #     styles = []
    #     for widget in self.findChildren(QWidget):
    #         styles.append(widget.styleSheet())
    #     print("\n".join(styles))
    #     return "\n".join(styles)
        

    def remove_stylesheets(self):
        # Iterate through all widgets and remove their stylesheets
        for widget in QApplication.instance().allWidgets():
            widget.setStyleSheet('')

    def dobleClickMaximizeRestore(self, event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: self.maximizeRestore())

    def removeTitleBar(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def maximizeRestore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.maxMinButton.setToolTip("Restore")
            self.maxMinButton.setIcon(QtGui.QIcon(u":/icons/cil-window-restore.png"))
            # self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.maxMinButton.setToolTip("Maximize")
            self.maxMinButton.setIcon(QtGui.QIcon(u":/icons/cil-window-maximize.png"))
            # self.ui.frame_size_grip.show()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton and event.y() < self.topFrame.height():
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def lightDarkModeUI(self):
        # Create a frame
        self.frame = QFrame(self)

        # Create a label
        self.labelLight = QLabel("Light Mode", self)

        self.toggle = PyToggle()

        # Create another label
        self.labelDark = QLabel("Dark Mode", self)

        # Create a horizontal layout
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.labelLight)
        self.horizontal_layout.addWidget(self.toggle)
        self.horizontal_layout.addWidget(self.labelDark)

        # Set the layout of the frame to the horizontal layout
        self.frame.setLayout(self.horizontal_layout)

        self.verticalLayout_2.addWidget(self.frame)

        self.toggle.stateChanged.connect(self.updateStylesheet)
        # toggle.stateChanged.connect(lambda state: self.updateStylesheet(state))

    def updateStylesheet(self, dark_mode):
        # Use the appropriate stylesheet based on the dark_mode parameter
        updated_stylesheet = Stylesheet.darkMode() if dark_mode else Stylesheet.lightMode()

        # Apply the stylesheet to the main window
        self.setStyleSheet(updated_stylesheet)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
