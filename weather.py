import requests
import json


class Weather_Api:
    def __init__(self, api="230a8f3c0468b38e1a667b3011ff0b85", city='Seoul'):
        self.apikey = api # https://openweathermap.org/ api얻기
        self.api = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+self.apikey

    def get_current_weather(self):
        url = self.api.format(key=self.apikey)
        r = requests.get(url)
        data = json.loads(r.text)
        return data["weather"][0]["description"]

        # print("+ 도시 =", data["name"])
        # print("| 날씨 =", data["weather"][0]["description"])
        # print("| 최저 기온 =", k2c(data["main"]["temp_min"]))
        # print("| 최고 기온 =", k2c(data["main"]["temp_max"]))
        # print("| 습도 =", data["main"]["humidity"])
        # print("| 기압 =", data["main"]["pressure"])
        # print("| 풍향 =", data["wind"]["deg"])
        # print("| 풍속 =", data["wind"]["speed"])
        # print("")