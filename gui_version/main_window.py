import numpy as np
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal, QObject
from PyQt5 import QtWidgets
from gtts import gTTS
from playsound import playsound

######################################
from video_window import Video_Window
from weather import Weather_Api
from music_window import Music_Window
######################################


class CommandSignals(QObject):
    command = pyqtSignal(str)


class Worker(QObject):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.signals = CommandSignals()
        print("One Thread has been started")

    @pyqtSlot(str)
    def say(self,sentence):
        print(sentence)
        tts = gTTS(text=sentence, lang='en')
        tts.save("./tmp/a.mp3")
        playsound("./tmp/a.mp3")


class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        loadUi("./Design/main_window.ui", self)
        self.youtube_button.clicked.connect(self.start_youtube_music)
        self.game_button.clicked.connect(self.start_game)
        self.weather_button.clicked.connect(self.get_weather_information)
        self.webcam_button.clicked.connect(self.start_webcam)
        self.input = self.findChild(QtWidgets.QLineEdit, 'chat_input_label')
        self.filename = "./tmp/a.mp3"
        self.signals = CommandSignals()
        self.worker = Worker()
        self.worker_thread = QThread()
        self.start_thread()
        self.music_window = None
        self.webcam_window = None

    def end_thread(self):
        if self.worker_thread.isRunning():
            self.worker_thread.terminate()

    def start_thread(self):
        self.signals.command.connect(self.worker.say)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            if not self.current_statue:
                self.print_chatting()
            else:
                return True

    @pyqtSlot()
    def start_youtube_music(self):
        self.chat_output_label.setText('starting youtube music')
        self.chat_output_label.adjustSize()
        if not self.music_window:
            self.music_window = Music_Window()
        self.music_window.show()

    @pyqtSlot()
    def start_game(self):
        self.chat_output_label.setText("Not Yet Ready")
        self.chat_output_label.adjustSize()

    @pyqtSlot()
    def get_weather_information(self):
        weather = Weather_Api()
        current_weather = weather.get_current_weather()
        self.signals.command.emit("Current weather is " + current_weather)
        self.chat_output_label.setText("Current weather is " + current_weather)
        self.chat_output_label.adjustSize()

    @pyqtSlot()
    def start_webcam(self):
        if not self.webcam_window:
            self.webcam_window = Video_Window()
        self.webcam_window.show()

    @pyqtSlot()
    def print_chatting(self):
        text = self.input.text()
        if text.lower() == 'weather':
            self.get_weather_information()
        elif text.lower() == 'game':
            self.start_game()
        elif text.lower() == 'youtube music':
            self.start_youtube_music()
        elif text.lower() == 'webcam':
            self.start_webcam()
        elif text.lower() == 'end_thread':
            self.signals2.command.emit("abc")
        else:
            self.chat_output_label.setText("This command is not in the list")
        self.chat_output_label.adjustSize()
        self.input.clear()
