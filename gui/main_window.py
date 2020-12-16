import os
import os.path
import numpy as np
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5 import QtWidgets
from gtts import gTTS
from playsound import playsound

######################################
from video_window import Video_Window
from weather import Weather_Api
from guessing_game import q_learning
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
        loadUi("main_window1.ui", self)
        self.youtube_button.clicked.connect(self.start_youtube_music)
        self.game_button.clicked.connect(self.start_game)
        self.weather_button.clicked.connect(self.get_weather_information)
        self.webcam_button.clicked.connect(self.start_webcam)
        self.input = self.findChild(QtWidgets.QLineEdit, 'chat_input_label')
        self.filename = "./tmp/a.mp3"
        self.signals = CommandSignals()
        self.signals2 = CommandSignals()
        self.worker = Worker()
        self.worker_thread = QThread()
        self.start_thread()
        self.current_statue = None
        self.MP = None
        self.new_window = None
        
    def end_thread(self):
        if self.worker_thread.isRunning():
            self.worker_thread.terminate()

    def start_thread(self):
        self.signals.command.connect(self.worker.say)
        self.signals2.command.connect(self.worker.music)
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
        self.current_statue = 'youtube music'
        self.statue.setText(self.current_statue)
        self.chat_output_label.setText('start_youtube_music')
        self.chat_output_label.adjustSize()
        self.current_statue = None

    @pyqtSlot()
    def start_game(self):
        if self.MP:
            self.MP.pause_vlc()
        if not self.worker_thread.isRunning():
            self.worker_thread.start()
        self.current_statue = 'game'
        self.statue.setText(self.current_statue)
        self.signals.command.emit("We have one game on this AI speaker. Do you want you play with me? If you want to hear how to play, please write 'how to play'")
        self.chat_output_label.setText('Please, Write yes, no or how to play.')
        self.chat_output_label.adjustSize()
        # self.delete()

        ans = 'how to play'

        while ans.lower() == 'yes':
            self.signals.command.emit("The game is initialized.")
            self.delete()
            GG = q_learning()
            GG.guess_number()
            current_number = GG.computer.first_digit
            chances = 20
            number = -1

            while chances > 0:
                self.signals.command.emit("Current number is %s. You have %s chance to guess the number" % (current_number, chances))
                self.delete()
                self.chat_output_label.setText(
                    "Current number is %s. You have %s chance to guess the number" % (current_number, chances))
                self.chat_output_label.adjustSize()
                if 0 < number < GG.answer.first_digit:
                    self.signals.command.emit("The answer number is greater than the number you've chosen.")
                    self.delete()
                elif GG.answer.first_digit < number <= 50:
                    self.signals.command.emit("The answer number is smaller than the number you've chosen.")
                    self.delete()
                chances -= 1
                obs = GG.computer - GG.answer
                choice = np.argmax(GG.q_table[obs])
                GG.computer.action(choice)
                number = input("number (1~50) :  ")
                number = int(number)
                current_number = number
                if number == GG.answer.first_digit:
                    self.signals.command.emit("You chose the number which is answer. You win.")
                    self.delete()
                    break
                if GG.computer.first_digit == GG.answer.first_digit:
                    self.signals.command.emit("You are defeated. I chose answer number before you.")
                    self.delete()
                    break

            ans = input('Please, Write yes, no or how to play.\n')

        if ans.lower() == 'how to play':
            self.signals.command.emit(
                "You have to guess the number which is randomly picked by numpy library. You just need to guess before me.")
            self.delete()
            self.signals.command.emit(
                "You have 20 chances to guess the number same as me. However, I can figure it out the number before you.")
            self.delete()
            self.signals.command.emit(
                "There will be starting number and I will tell you whether this number is lower than the answer number or not")
            self.delete()
            self.signals.command.emit("The number is between 1 to 50.")
            self.delete()

        self.current_statue = None

    @pyqtSlot()
    def get_weather_information(self):
        weather = Weather_Api()
        current_weather = weather.get_current_weather()
        self.signals.command.emit("Current weather is " + current_weather)
        self.chat_output_label.setText("Current weather is " + current_weather)
        self.chat_output_label.adjustSize()

    @pyqtSlot()
    def start_webcam(self):
        self.new_window = Video_Window()
        self.new_window.show()

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
            self.end_thread()
        else:
            self.chat_output_label.setText("This command is not in the list")
        self.chat_output_label.adjustSize()
        self.input.clear()
