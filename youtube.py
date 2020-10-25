import pafy
import re
from googleapiclient.discovery import build
import collections


class Youtube_Player:
    def __init__(self, maximum=1, flag=False):
        self.DEVELOPER_KEY = 'AIzaSyAuOaIjo2G-hugN6uM_XnOcJyziy74TJQw'
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'
        self.maximum = maximum
        self.flag = flag
        self.cnt = 0

    def check(self, readData):
        for text in readData:
            text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
            if text.lower() in ['lyrics','audio']:
                return True

        return False

    def youtube_stream_link(self, videos):
        if self.maximum == 1:
            url = 'https://www.youtube.com/watch?v='+str(videos[1][0][-11:])
            video = pafy.new(url)
            best_audio = video.getbestaudio()
            audio_streaming_link = best_audio.url
            videos[1].append(audio_streaming_link)
        else:
            if self.flag:
                self.cnt = len(videos)
                x = self.cnt
                while self.cnt < len(videos) + x:
                    self.cnt += 1
                    url = 'https://www.youtube.com/watch?v=' + str(videos[self.cnt][0][-11:])
                    video = pafy.new(url)
                    best_audio = video.getbestaudio()
                    audio_streaming_link = best_audio.url
                    videos[self.cnt].append(audio_streaming_link)
            else:
                self.cnt = 0
                while self.cnt < len(videos):
                    self.cnt += 1
                    url = 'https://www.youtube.com/watch?v=' + str(videos[self.cnt][0][-11:])
                    video = pafy.new(url)
                    best_audio = video.getbestaudio()
                    audio_streaming_link = best_audio.url
                    videos[self.cnt].append(audio_streaming_link)

        return videos

    def search(self, query):
        youtube_client = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)

        search_response = youtube_client.search().list(
            q = query,
            part = 'id, snippet'
        ).execute()

        videos = collections.defaultdict(list)

        if self.flag:
            pass
        else:
            self.cnt = 0

        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                if self.check(search_result['snippet']['title'].split()):
                    self.cnt += 1
                    videos[self.cnt].append('%s %s' % (search_result['snippet']['title'],
                                               search_result['id']['videoId']))

        if len(videos) != 0:
            audio_streaming_link = self.youtube_stream_link(videos)
            return audio_streaming_link


if __name__ == '__main__':
    y = Youtube_Player()
    y.search(query='sicko mode')