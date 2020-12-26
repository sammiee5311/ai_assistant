from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5 import QtWidgets

######################################
from youtube import Youtube_Player
from music_player import Music_Player
######################################


class Music_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Music_Window, self).__init__()
        loadUi("./Design/music_window.ui", self)
        self.resume_button.clicked.connect(self.resume)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
        self.search_button.clicked.connect(self.search_music)
        self.next_song_button.clicked.connect(self.next_song)
        self.playlist_button.clicked.connect(self.playlist)
        self.input = self.findChild(QtWidgets.QLineEdit, 'input_label')
        self.YT = Youtube_Player(maximum=3)
        self.MP = None
        self.playlist = ''
        self.music = 'None'

    @pyqtSlot()
    def next_song(self):
        self.MP.stop_vlc()
        self.MP.next_song()

    @pyqtSlot()
    def playlist(self):
        cur, playlist = self.MP.show_playlist()
        self.music_name.setWordWrap(True)
        self.music_name.setText(cur)
        self.music_name.adjustSize()
        for i, music in enumerate(playlist):
            if len(music) == 2:
                self.music_name.setText(music[0][:-11])

    @pyqtSlot()
    def resume(self):
        self.MP.play_vlc()
        self.music_name.setText(self.music)
        self.music_name.adjustSize()

    @pyqtSlot()
    def pause(self):
        self.MP.pause_vlc()
        self.music_name.setText("Music is paused")
        self.music_name.adjustSize()

    @pyqtSlot()
    def stop(self):
        self.MP.stop_vlc()
        self.music_name.setText("Music is stopped")
        self.music_name.adjustSize()

    @pyqtSlot()
    def search_music(self):
        self.music = self.input.text()
        self.YT.is_existed_playlist = False
        playlist = self.YT.search(self.music)
        if not playlist:
            self.music_name.setText("Sorry, there is not %s on youtube")
            self.music_name.adjustSize()
        else:
            self.MP = Music_Player(playlist, maximum=10)
            self.MP.youtube_player()
            self.music_name.setText(self.music)
            self.music_name.adjustSize()

        self.input.clear()


