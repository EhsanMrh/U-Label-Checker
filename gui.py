import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets
import time
from mediaPlayerWithPlaylist import VideoPlayer


class MainWindow(QMainWindow):

    def __init__(self, exit_app):
        super().__init__()
        self.exit_app = exit_app
        self.title = 'Main Window'
        self.left = 400
        self.top = 200
        self.width = 700
        self.height = 700
        self.initUI()
        self.VideoPlayerWindow = None

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.header = QLabel("Enter your name:", self)
        self.header.move(290, 150)
        self.header.resize(500, 60)

        # Create textbox
        self.name = QLineEdit(self)
        self.name.move(200, 200)
        self.name.resize(280, 40)

        # Create a button in the window
        self.StartBTN = QPushButton('Start', self)
        self.StartBTN.move(290, 250)

        # connect button to function on_click
        self.StartBTN.clicked.connect(self.StartBTN_on_click)
        self.show()

    def enable_StartBTN(self):
        self.StartBTN.setDisabled(False)

    def StartBTN_on_click(self):
        textboxValue = self.name.text()
        if self.VideoPlayerWindow is None and textboxValue:
            # path = self.createDirectory(textboxValue)
            self.VideoPlayerWindow = VideoPlayer(textboxValue, self.enable_StartBTN, self.setVideoPlayerNone, self.exit_app)
            self.StartBTN.setEnabled(False)
            self.VideoPlayerWindow.setWindowTitle("Player")
            self.VideoPlayerWindow.resize(700, 700)
            self.VideoPlayerWindow.show()

    def setVideoPlayerNone(self):
        self.VideoPlayerWindow = None


