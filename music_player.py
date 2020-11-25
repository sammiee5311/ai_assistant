import vlc
from youtube import Youtube_Player
import os
import time
import json


class Music_Player:
    def __init__(self, playlist, maximum=1):
        self.instance = vlc.Instance('--verbose 0')
        self.playlist = playlist
        self.maximum = maximum
        self.track_number = 0
        self.current_music = None

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
        self.track_number += 1
        if self.track_number in self.playlist:
            self.current_music = self.playlist[self.track_number][0][:-11]
            music = self.playlist[self.track_number].pop()
            while music[8:16] == 'manifest':
                if self.track_number < len(self.playlist):
                    self.track_number += 1
                    self.current_music = self.playlist[self.track_number][0][:-11]
                    music = self.playlist[self.track_number].pop()

            self.play(music)

    def end_callback(self, event):
        current_track_number = self.track_number
        playlist_size = len(self.playlist)
        if current_track_number <= playlist_size and self.track_number - 1 < self.maximum:
            self.youtube_player()

    def next_song(self):
        self.youtube_player()

    def show_playlist(self):
        print('[C] %s' % self.current_music)
        for i, music in enumerate(self.playlist.values()):
            if len(music) == 2:
                print('%s' % music[0][:-11])

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
    tracks = YT.search('')

    MP = Music_Player(tracks)
    MP.youtube_player()
