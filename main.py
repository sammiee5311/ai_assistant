from gtts import gTTS
import os
import os.path
import numpy as np
from playsound import playsound

#####################################
from music_player import Music_Player
from youtube import Youtube_Player
from guessing_game import q_learning
from weather import Weather_Api
#####################################


class speaker:
    def __init__(self):
        self.filename = "./tmp/a.mp3"
        self.MP = None

    def say(self,sentence):
        tts = gTTS(text=sentence, lang='en')
        tts.save(self.filename)
        playsound(self.filename)

    def main(self, text):
        if text == 'youtube':
            YT.is_existed_playlist = False
            self.say("Please, write music\'s name")
            self.delete()
            music = input()
            playlist = YT.search(str(music))
            if not playlist:
                self.say("Sorry, there is not %s on youtube" % str(music))
                self.delete()
            else:
                self.MP = Music_Player(playlist,maximum=10)
                self.MP.youtube_player()

        elif text == 'add music' and self.MP:
            YT.is_existed_playlist = True
            self.MP.pause_vlc()
            self.say("Please, write music\'s name")
            self.delete()
            music = input()
            playlist_ = YT.search(str(music),len(self.MP.playlist))
            if not playlist_:
                self.say("Sorry, there is not %s on youtube" % str(music))
                self.delete()
                self.MP.play_vlc()
            else:
                self.MP.playlist = {**self.MP.playlist, **playlist_}
                self.say("Music is added to your playlist")
                self.delete()
                self.MP.play_vlc()

        elif text == 'resume music' and self.MP:
            self.say("Music will be started soon again")
            self.delete()
            self.MP.play_vlc()

        elif text == 'show playlist' and self.MP:
            self.MP.show_playlist()

        elif text == 'pause music' and self.MP:
            self.MP.pause_vlc()
            self.say("Music is paused")
            self.delete()

        elif text == 'stop music' and self.MP:
            self.MP.stop_vlc()
            self.say("Music is stopped")
            self.delete()

        elif text == 'next music' and self.MP:
            self.MP.stop_vlc()
            self.say("Music will be changed in a moment")
            self.delete()
            self.MP.next_song()

        elif text == 'weather':
            if self.MP:
                self.MP.pause_vlc()
                current_weather = WA.get_current_weather()
                self.say("Current weather is %s" % current_weather)
                self.delete()
                self.MP.play_vlc()
            else:
                current_weather = WA.get_current_weather()
                self.say("Current weather is %s" % current_weather)
                self.delete()

        elif text == 'play':
            if self.MP:
                self.MP.pause_vlc()
            self.say("We have one game on this AI speaker. Do you want you play with me? If you want to hear how to play, please write 'how to play'")
            self.delete()
            ans = input('Please, Write yes, no or how to play.\n')

            while ans.lower() == 'yes':
                self.say("The game is initialized.")
                self.delete()
                GG = q_learning()
                GG.guess_number()
                current_number = GG.computer.first_digit
                chances = 20
                number = -1

                while chances > 0:
                    self.say("Current number is %s. You have %s chance to guess the number" %(current_number, chances))
                    print("Current number is %s. You have %s chance to guess the number" %(current_number, chances))
                    self.delete()
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
                self.say("You have to guess the number which is randomly picked by numpy library. You just need to guess before me.")
                self.delete()
                self.say("You have 20 chances to guess the number same as me. However, I can figure it out the number before you.")
                self.delete()
                self.say("There will be starting number and I will tell you whether this number is lower than the answer number or not")
                self.delete()
                self.say("The number is between 1 to 50.")
                self.delete()

        elif text == 'question':
            ques = "a"
            while ques.lower() != 'nothing':
                if ques.lower() != "a":
                    self.say("Do you have other question?")
                    self.delete()
                else:
                    self.say("What is your question?")
                    self.delete()
                ques = input("question : ")
            self.say("Question end")
            self.delete()

        elif text == 'morning':
            self.say("Good morning ! How are you?")
            self.delete()

    def delete(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)


if __name__ == '__main__':
    sp = speaker()
    YT = Youtube_Player(maximum=3)
    WA = Weather_Api()
    start_q_table = {}

    while True:
        text = input("write command here\n")
        if text.lower() == 'quit':
            break

        sp.main(text.lower())
