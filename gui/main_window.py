import os
import os.path
import numpy as np
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
from PyQt5 import QtWidgets
from gtts import gTTS
from playsound import playsound

######################################
from video_window import Video_Window
from weather import Weather_Api
from guessing_game import q_learning
######################################


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
        self.current_statue = None
        self.MP = None
        self.new_window = None

    def say(self,sentence):
        tts = gTTS(text=sentence, lang='en')
        tts.save(self.filename)
        playsound(self.filename)

    def delete(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)

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
        self.current_statue = 'game'
        self.statue.setText(self.current_statue)
        # self.say(
        #     "We have one game on this AI speaker. Do you want you play with me? If you want to hear how to play, please write 'how to play'")
        self.chat_output_label.setText('Please, Write yes, no or how to play.')
        self.chat_output_label.adjustSize()
        self.delete()

        ans = self.input.text()

        while ans.lower() == 'yes':
            self.say("The game is initialized.")
            self.delete()
            GG = q_learning()
            GG.guess_number()
            current_number = GG.computer.first_digit
            chances = 20
            number = -1

            while chances > 0:
                self.say("Current number is %s. You have %s chance to guess the number" % (current_number, chances))
                self.delete()
                self.chat_output_label.setText(
                    "Current number is %s. You have %s chance to guess the number" % (current_number, chances))
                self.chat_output_label.adjustSize()
                if 0 < number < GG.answer.first_digit:
                    self.say("The answer number is greater than the number you've chosen.")
                    self.delete()
                elif GG.answer.first_digit < number <= 50:
                    self.say("The answer number is smaller than the number you've chosen.")
                    self.delete()
                chances -= 1
                obs = GG.computer - GG.answer
                choice = np.argmax(GG.q_table[obs])
                GG.computer.action(choice)
                number = input("number (1~50) :  ")
                number = int(number)
                current_number = number
                if number == GG.answer.first_digit:
                    self.say("You chose the number which is answer. You win.")
                    self.delete()
                    break
                if GG.computer.first_digit == GG.answer.first_digit:
                    self.say("You are defeated. I chose answer number before you.")
                    self.delete()
                    break

            ans = input('Please, Write yes, no or how to play.\n')

        if ans.lower() == 'how to play':
            self.say(
                "You have to guess the number which is randomly picked by numpy library. You just need to guess before me.")
            self.delete()
            self.say(
                "You have 20 chances to guess the number same as me. However, I can figure it out the number before you.")
            self.delete()
            self.say(
                "There will be starting number and I will tell you whether this number is lower than the answer number or not")
            self.delete()
            self.say("The number is between 1 to 50.")
            self.delete()

        self.current_statue = None

    @pyqtSlot()
    def get_weather_information(self):
        weather = Weather_Api()
        current_weather = weather.get_current_weather()
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
        else:
            self.chat_output_label.setText("This command is not in the list")
        self.chat_output_label.adjustSize()
        self.input.clear()
