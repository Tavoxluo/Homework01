import requests
import json


def get_weather(city_name):
    url = "http://wttr.in/{}".format(city_name)
    response_txt = requests.get(url).text
    # json_data = json.loads(response.text)
    print(response_txt)


if __name__ == '__main__':
    get_weather("beijing")