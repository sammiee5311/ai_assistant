from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5 import QtWidgets

from video_window import Video_Window


class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        loadUi("main_window.ui", self)
        self.youtube_button.clicked.connect(self.start_youtube_music)
        self.game_button.clicked.connect(self.start_game)
        self.weather_button.clicked.connect(self.get_weather_information)
        self.webcam_button.clicked.connect(self.start_webcam)
        self.input = self.findChild(QtWidgets.QLineEdit, 'chat_input_label')
        self.send_button.clicked.connect(self.print_chatting)
        self.new_window = None

    @pyqtSlot()
    def start_youtube_music(self):
        self.chat_output_label.setText('start youtube music')
        self.chat_output_label.adjustSize()

    @pyqtSlot()
    def start_game(self):
        self.chat_output_label.setText('start game')
        self.chat_output_label.adjustSize()

    @pyqtSlot()
    def get_weather_information(self):
        self.chat_output_label.setText('get weather information')
        self.chat_output_label.adjustSize()

    @pyqtSlot()
    def start_webcam(self):
        self.new_window = Video_Window()
        self.new_window.show()

    @pyqtSlot()
    def print_chatting(self):
        self.chat_output_label.setText(self.input.text())
        self.chat_output_label.adjustSize()




