import os
import time

import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *

from directions import VIDEO_DIR


class VideoPlayer(QtWidgets.QWidget):
    def __init__(self, name, enable_start, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.name = name
        self.enable_start = enable_start

        self.result = {
            'path': [],
            'word': []
        }

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.selected_word = None
        self.video_duration = 1

        btnSize = QSize(16, 16)
        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.start_play)

        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.statusBar)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("Ready")

    def showInputBox(self, path, word):
        input_word, done = QtWidgets.QInputDialog.getText(
            self, 'Input', 'Enter Correct Word:', text=word)
        if input_word and done:
            self.result['path'].append(path)
            self.result['word'].append(input_word)
        else:
            self.result['path'].append(path)
            self.result['word'].append('None')

    def create_personal_dir(self, path):
        personal_directory = f'results/{path}'
        if os.path.exists(personal_directory):
            directories = os.listdir(personal_directory)
            if directories:
                directories.sort()
                last_session_index = int(directories[-1].split(' ')[1]) + 1

                os.mkdir(f'{personal_directory}/session {last_session_index}')
                destination = f'{personal_directory}/session {last_session_index}'
            else:
                os.mkdir(f'{personal_directory}/session 1')
                destination = f'{personal_directory}/session 1'

        else:
            os.mkdir(personal_directory)
            os.mkdir(f'{personal_directory}/session 1')
            destination = f'{personal_directory}/session 1'

        return destination

    def start_play(self):
        word_list = os.listdir(VIDEO_DIR)
        for word in word_list:
            self.selected_word = word
            sample_list = os.listdir(f'{VIDEO_DIR}/{word}')
            for sample in sample_list:
                print("Sample: ", sample)
                video_relpath = f'{VIDEO_DIR}/{word}/{sample}'
                video_abspath = os.path.abspath(f'{VIDEO_DIR}/{word}/{sample}')
                self.abrir(video_abspath, video_relpath, word)

        dataframe = pd.DataFrame(self.result)
        if not os.path.exists('results'):
            os.mkdir('results')
        des = self.create_personal_dir(self.name)

        dataframe.to_csv(f'{des}/result.csv')
        print("file saved")

        self.enable_start()
        self.close()

    def abrir(self, absolute_path, relative_path, word):
        fileName = absolute_path
        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.play()
            time.sleep(int(np.ceil(self.video_duration / 1000)))
            self.showInputBox(relative_path, self.selected_word)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def durationChanged(self, duration):
        self.video_duration = duration

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())


