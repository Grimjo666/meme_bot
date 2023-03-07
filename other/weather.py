import requests
from math import floor

from config import O_W_TOKEN


# function to convert city name to coordinates
def city_cord(city, api_key=O_W_TOKEN):

    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={1}&appid={api_key}')
    data = response.json()
    lat = data[0]['lat']
    lon = data[0]['lon']
    return lat, lon


# we get a dict with information about the weather for 5 days
def get_weather_dict(coord, api_key=O_W_TOKEN) -> dict:
    weather_dict = {}

    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/forecast?lat={coord[0]}&lon={coord[1]}&appid={api_key}&units=metric&lang={"ru"}')
    data = response.json()
    for item in data['list']:
        weather_dict[item['dt_txt']] = f"Температура: {floor(item['main']['temp'])}\n" \
                                       f"Ощущается как: {floor(item['main']['feels_like'])}\n" \
                                       f"{item['weather'][0]['description']}\n" \
                                       f"'Скорость ветра:' {item['wind']['speed']} М/С"

    return weather_dict


# print(get_weather_dict(city_cord(input())))
