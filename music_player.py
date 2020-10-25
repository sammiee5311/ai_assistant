import vlc
from youtube import Youtube_Player
import os
import time
import json


class Music_Player:
    def __init__(self, tracks, maximum=1):
        self.instance = vlc.Instance('--verbose 0')
        self.tracks = tracks
        self.maximum = maximum
        self.cnt = 0
        self.current_song = None

    def play(self,url):
        self.player = self.instance.media_player_new()
        media = self.instance.media_new(url)
        media.get_mrl()
        self.player.set_media(media)
        self.player.play()

        time.sleep(5)
        event_manager = self.player.event_manager()
        event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.end_callback)

    def youtube_player(self):
        self.cnt += 1
        if self.cnt in self.tracks:
            self.current_song = self.tracks[self.cnt][0][:-11]
            track = self.tracks[self.cnt].pop()
            while track[8:16] == 'manifest':
                if self.cnt < len(self.tracks):
                    self.cnt += 1
                    self.current_song = self.tracks[self.cnt][0][:-11]
                    track = self.tracks[self.cnt].pop()

            self.play(track)

    def end_callback(self, event):
        currenttrackid = self.cnt
        numtracks = len(self.tracks)
        if currenttrackid <= numtracks and self.cnt - 1 < self.maximum:
            self.youtube_player()

    def next_song(self):
        self.youtube_player()

    def show_playlist(self):
        print('1[C] %s' % self.current_song)
        for i, song in enumerate(self.tracks.values()):
            if len(song) == 2:
                print('%d %s' % (i+1, song[0][:-11]))

    def set_vlc_volume(self, level):
        self.player.audio_set_volume(level)

    def get_vlc_volume(self):
        return self.player.audio_get_volume()

    def mute_vlc(self, status=True):
        return self.player.audio_set_mute(status)

    def stop_vlc(self):
        print('stopping vlc')
        self.player.stop()

    def pause_vlc(self):
        print('pausing vlc')
        self.player.pause()

    def play_vlc(self):
        if self.player.get_state() == vlc.State.Paused:
            print('playing/resuming vlc')
            self.player.play()

    def is_vlc_playing(self):
        return self.player.is_playing()

    def state(self):
        return self.player.get_state()

if __name__ == '__main__':
    YT = Youtube_Player()
    tracks = YT.search('toosie')

    MP = Music_Player(tracks)
    MP.youtube_player()