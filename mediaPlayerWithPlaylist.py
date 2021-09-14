import os
import shutil
import csv

import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *

from config import VIDEO_PATH, RESULT_PATH, NOISE_PATH


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
            'path': '',
            'word': ''
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
        # Create noise directory
        if not os.path.exists(NOISE_PATH):
            os.mkdir(NOISE_PATH)

        input_word, done = QtWidgets.QInputDialog.getText(
            self, 'Input', 'Enter Correct Word:', text=self.selected_word)
        if input_word and done:
            self.result['path'] = (self.relative_path)
            self.result['word'] = (input_word)
        else:
            self.result['path'] = (self.relative_path)
            self.result['word'] = ('None')
            
            if not os.path.exists(f"{NOISE_PATH}/{self.selected_word}"):
                os.mkdir(f"{NOISE_PATH}/{self.selected_word}")
            source = f"{VIDEO_PATH}/{self.selected_word}/{self.relative_path}"
            print("Source: ", source)
            destination = f"{NOISE_PATH}/{self.selected_word}/{self.relative_path}"
            print("des: ", destination)
            shutil.move(source, destination)

            # self.exit_app()

    def handle_csv(self, path, word):
        fieldnames = ['path', 'word']

        if not os.path.isfile(f'{RESULT_PATH}/{self.name}.csv'):
            processed_file = open(f'{RESULT_PATH}/{self.name}.csv', mode='a+')        
            processed_file_writer = csv.DictWriter(processed_file, fieldnames=fieldnames)
            processed_file_writer.writeheader()
            processed_file.flush()

        else:
            processed_file = open(f'{RESULT_PATH}/{self.name}.csv', mode='a+')        
            processed_file_writer = csv.DictWriter(processed_file, fieldnames=fieldnames)


        processed_file_writer.writerow({'path': path, 
                                        'word': word})
        processed_file.flush()
        processed_file.close()


    def endMedia(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.showInputBox()
            # Check and create results file
            if not os.path.exists(RESULT_PATH):
                os.mkdir(RESULT_PATH)

            # Write to csv file
            self.handle_csv(self.result['path'],self.result['word'])
                
            print(f"+ Label: '{self.result['word']}'  for video: '{self.result['path']}'  saved! ")
 
            if self.current_index == self.playlist_media_count:
                self.enable_start()
                self.close()
                self.setVideoPlayerNone()

    def videoChanged(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
            self.selected_word = url.path().split('/')[-2]
            self.relative_path = url.fileName()

    def importVideoPlaylist(self):
        word_list = os.listdir(VIDEO_PATH)
        self.selected_word = word_list[0]
        labeled_videos_path = f"{RESULT_PATH}/{self.name}.csv"
        labeled_videos = ''
        if os.path.isfile(labeled_videos_path):
            labeled_videos = pd.read_csv(labeled_videos_path)

        for word in word_list:
            sample_list = os.listdir(f'{VIDEO_PATH}/{word}')
            for sample in sample_list:
                if len(labeled_videos):
                    if (len(labeled_videos[labeled_videos['path'] == sample]) == 0):
                        video_abspath = os.path.abspath(f'{VIDEO_PATH}/{word}/{sample}')
                        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(video_abspath)))
                else: 
                    video_abspath = os.path.abspath(f'{VIDEO_PATH}/{word}/{sample}')
                    self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(video_abspath)))

        if not self.playlist.isEmpty():
            self.playlist_media_count = self.playlist.mediaCount()
            self.mediaPlayer.setPlaylist(self.playlist)
        else:
            print("All videos labeled")
            self.exit_app()

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
