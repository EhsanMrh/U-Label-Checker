import os
import re
import time

import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *

from directions import VIDEO_DIR


def createPersonalDir(path):
    personal_directory = f'results/{path}'
    if os.path.exists(personal_directory):
        directories = os.listdir(personal_directory)
        if directories:
            indexes = [int(index.split(' ')[1]) for index in directories]

            os.mkdir(f'{personal_directory}/session {max(indexes) + 1}')
            destination = f'{personal_directory}/session {max(indexes) + 1}'
        else:
            os.mkdir(f'{personal_directory}/session 1')
            destination = f'{personal_directory}/session 1'

    else:
        os.mkdir(personal_directory)
        os.mkdir(f'{personal_directory}/session 1')
        destination = f'{personal_directory}/session 1'

    return destination


class VideoPlayer(QtWidgets.QWidget):
    def __init__(self, name, enable_start, setVideoPlayerNone, exit_app, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.name = name
        self.enable_start = enable_start
        self.setVideoPlayerNone = setVideoPlayerNone
        self.exit_app = exit_app

        self.selected_word = None
        self.relative_path = None
        self.video_duration = 1
        self.playlist_media_count = 0
        self.current_index = 0
        self.result = {
            'path': [],
            'word': []
        }

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        btnSize = QSize(16, 16)
        videoWidget = QVideoWidget()

        # Playlist
        self.playlist = QMediaPlaylist()
        self.playlist.currentMediaChanged.connect(self.videoChanged)
        self.playlist.currentIndexChanged.connect(self.playlistIndexChange)

        self.playButton = QPushButton()
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.startPlay)

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
        self.mediaPlayer.mediaStatusChanged.connect(self.endMedia)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("Ready")

    def showInputBox(self):
        input_word, done = QtWidgets.QInputDialog.getText(
            self, 'Input', 'Enter Correct Word:', text=self.selected_word)
        if input_word and done:
            self.result['path'].append(self.relative_path)
            self.result['word'].append(input_word)
        else:
            self.result['path'].append(self.relative_path)
            self.result['word'].append('None')
            self.exit_app()

    def endMedia(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.showInputBox()
            if self.current_index == self.playlist_media_count:
                dataframe = pd.DataFrame(self.result)
                if not os.path.exists('results'):
                    os.mkdir('results')
                des = createPersonalDir(self.name)

                dataframe.to_csv(f'{des}/result.csv')
                print("+ file saved")

                self.enable_start()
                self.close()
                self.setVideoPlayerNone()

    def videoChanged(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
            self.selected_word = url.path().split('/')[-2]
            self.relative_path = url.fileName()

    def importVideoPlaylist(self):
        word_list = os.listdir(VIDEO_DIR)
        self.selected_word = word_list[0]
        for word in word_list:
            sample_list = os.listdir(f'{VIDEO_DIR}/{word}')
            for sample in sample_list:
                video_abspath = os.path.abspath(f'{VIDEO_DIR}/{word}/{sample}')
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(video_abspath)))

        self.playlist_media_count = self.playlist.mediaCount()
        self.mediaPlayer.setPlaylist(self.playlist)

    def playlistIndexChange(self, index):
        self.current_index = index + 1
        print(f"{self.current_index} of {self.playlist_media_count} videos")

    def startPlay(self):
        self.importVideoPlaylist()
        self.play()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setEnabled(False)

    def durationChanged(self, duration):
        self.video_duration = duration

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())
