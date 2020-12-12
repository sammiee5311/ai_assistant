import requests
import json


class Weather_Api:
    def __init__(self, api="", city='Seoul'):
        self.apikey = api
        self.api = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+self.apikey

    def get_current_weather(self):
        url = self.api.format(key=self.apikey)
        r = requests.get(url)
        data = json.loads(r.text)
        return data["weather"][0]["description"]
