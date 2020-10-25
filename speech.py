from gtts import gTTS
import os
import os.path
from music_player import Music_Player
import music_player
from youtube import Youtube_Player
import time

from playsound import playsound


# p = vlc.MediaPlayer("file://abc.mp3")
# # p.play()

# google api key = AIzaSyAuOaIjo2G-hugN6uM_XnOcJyziy74TJQw
# spotify api key = BQCj8czpQ-kszM3TN4zFYkvT_Euuh24HMG-t16P6_MT3m822TLjjE7DL-dyFfjAWzzXHHF-iBvvZwyZAnGyRcsw-QXApn_kEGT7sX568HHx182rwLHZ2FqikE6ndfKm9bU7i8bbnC6qWpHrM57Sf6UIX

class speaker:
    def __init__(self):
        self.filename = "./tmp/a.mp3"

    def say(self,sentence):
        tts = gTTS(text=sentence, lang='en')
        tts.save(self.filename)
        playsound(self.filename)

    def main(self, text):
        if text == 'youtube':
            YT.flag = False
            self.say("Please, write song\'s name")
            self.delete()
            song = input()
            tracks = YT.search(str(song))
            if not tracks:
                self.say("Sorry, there is not %s on youtube" % str(song))
                self.delete()
            else:
                self.MP = Music_Player(tracks,maximum=3)
                self.MP.youtube_player()

        if text == 'add music':
            YT.flag = True
            self.MP.pause_vlc()
            self.say("Please, write song\'s name")
            self.delete()
            song = input()
            tracks2 = YT.search(str(song))
            if not tracks2:
                self.say("Sorry, there is not %s on youtube" % str(song))
                self.delete()
                self.MP.play_vlc()
            else:
                self.MP.tracks = {**self.MP.tracks, **tracks2}
                self.say("Music is added to your playlist")
                self.delete()
                self.MP.play_vlc()

        if text == 're-start music':
            self.say("Music will be started soon again")
            self.delete()
            self.MP.play_vlc()

        if text == 'show playlist':
            self.MP.show_playlist()

        if text == 'pause music':
            self.MP.pause_vlc()
            self.say("Music is paused")
            self.delete()

        if text == 'stop music':
            self.MP.stop_vlc()
            self.say("Music is stopped")
            self.delete()

        if text == 'next song':
            self.MP.stop_vlc()
            self.say("Music will be changed in a moment")
            self.delete()
            self.MP.next_song()

        if text == 'question':
            ques = "a"
            while ques.lower() != 'nothing':
                if ques.lower() != "a":
                    self.say("Do you have other question?")
                    self.delete()
                else:
                    self.say("What is your question?")
                    self.delete()
                ques = input("question : ")
                if "cammy" in ques.lower():
                    self.say("Cammy is a beautiful girl who is sammy's girlfriend.")
                    self.delete()
            self.say("Question end")
            self.delete()

        if text == 'morning':
            self.say("Good morning ! How are you, sammy?")
            self.delete()

    def delete(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)


if __name__ == '__main__':
    sp = speaker()
    YT = Youtube_Player(maximum=3)

    while True:
        text = input("write command here\n")

        if text.lower() == 'delete':
            sp.delete()

        else:
            sp.main(text.lower())