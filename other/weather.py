import requests
from math import floor

from database.dicts import weather_icons
from config import O_W_TOKEN


# function to convert city name to coordinates
def city_cord(city, api_key=O_W_TOKEN):

    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={1}&appid={api_key}')
    data = response.json()
    lat = data[0]['lat']
    lon = data[0]['lon']
    return lat, lon


# we get a dict with information about the weather for 5 days
def get_weather_dict(coord, api_key=O_W_TOKEN) -> list:
    weather_list = []

    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/forecast?lat={coord[0]}&lon={coord[1]}&appid={api_key}&units=metric&lang={"ru"}')
    data = response.json()
    for item in data['list']:
        weather_list.append((item['dt_txt'], f"Температура:  {floor(item['main']['temp'])} °C\n" \
                                       f"Ощущается как:  {floor(item['main']['feels_like'])} °C\n" \
                                       f"Скорость ветра:  {item['wind']['speed']} М/С\n" \
                                       f"{item['weather'][0]['description'].title()} {weather_icons[item['weather'][0]['icon']]}"))

    return weather_list


# print(get_weather_dict(city_cord(input())))
