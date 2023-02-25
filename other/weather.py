import requests
from math import floor


# function to convert city name to coordinates
def city_cord(api_key, city):

    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={1}&appid={api_key}')
    data = response.json()
    lat = data[0]['lat']
    lon = data[0]['lon']
    return lat, lon


# we get a dict with information about the weather for 5 days
def get_weather_dict(api_key, coord) -> dict:
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


# print(get_weather_dict(O_W_TOKEN, city_cord(O_W_TOKEN, input())))
