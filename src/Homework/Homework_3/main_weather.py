import os
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Any

import matplotlib.pyplot as plt
import requests

from src.Homework.Homework_3.orm import ORMMeta

URL = "https://api.openweathermap.org/data/2.5"
API_KEY = os.getenv("WEATHER_API_KEY")


@dataclass
class Weather(metaclass=ORMMeta):
    id: int
    main: str
    description: str
    icon: str


@dataclass
class Temperature(metaclass=ORMMeta):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: int
    sea_level: int
    grnd_level: int


@dataclass
class Wind(metaclass=ORMMeta):
    speed: float
    deg: int
    gust: float


@dataclass
class Personal_Weather(metaclass=ORMMeta):
    main: Temperature
    weather: Weather
    wind: Wind
    dt_txt: str


def get_json(url: str) -> dict[str, Any] | None:
    response = requests.get(url)
    data = response.json()
    if data.get("cod") != "404":
        return data
    print("<Error> Wrong city name")


def show_plot_figure(city_name: str, indicator: str, list_date: list[str], list_indicator: list[Any]) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(list_date, list_indicator, marker="o", color="b", linestyle="-")

    plt.title(f"{city_name}: {indicator.title()}")
    plt.xlabel("Dates")
    plt.ylabel(indicator.title())
    plt.grid(True)

    plt.show()


def show_plot_bar(list_date: list[str], list_speed: list[float], list_gust: list[float]) -> None:
    bar_width = 0.35
    x_indexes = range(5)

    plt.bar(x_indexes, list_speed, width=bar_width, color="blue", label="Speed")
    plt.bar([i + bar_width for i in x_indexes], list_gust, width=bar_width, color="orange", label="Gust")

    plt.xlabel("Dates")
    plt.ylabel("Wind Speed")
    plt.title("Gust")
    plt.xticks([index + bar_width / 2 for index in x_indexes], list_date)
    plt.legend()

    plt.show()


def get_weather(city_name: str) -> None:
    data = get_json(f"{URL}/weather?q={city_name}&units=metric&appid={API_KEY}")
    if data is None:
        return
    data["weather"] = data["weather"][0]
    orm = Personal_Weather.parse_json(data)
    print(f"<{city_name}> Current weather: {orm.weather.main}, description: {orm.weather.description}")


def get_temperature(city_name: str) -> None:
    data = get_json(f"{URL}/weather?q={city_name}&units=metric&appid={API_KEY}")
    if data is None:
        return
    orm = Personal_Weather.parse_json(data)
    print(f"<{city_name}> Current temperature: {orm.main.temp}°C, feels like: {orm.main.feels_like}°C")


def get_plot_temperature(city_name: str, indicator: str) -> None:
    data = get_json(f"{URL}/forecast?q={city_name}&units=metric&appid={API_KEY}")
    if data is None:
        return
    list_date, list_indicator = [], []
    for date_data in data["list"][0:5]:
        current_orm = Personal_Weather.parse_json(date_data)
        list_indicator.append(getattr(current_orm.main, indicator))
        list_date.append(current_orm.dt_txt.split()[1])
    show_plot_figure(city_name, indicator, list_date, list_indicator)


def get_plot_weather(city_name: str) -> None:
    data = get_json(f"{URL}/forecast?q={city_name}&units=metric&appid={API_KEY}")
    if data is None:
        return
    list_date, list_speed, list_gust = [], [], []
    for date_data in data["list"][0:5]:
        current_orm = Personal_Weather.parse_json(date_data)
        list_speed.append(getattr(current_orm.wind, "speed"))
        list_gust.append(getattr(current_orm.wind, "gust"))
        list_date.append(current_orm.dt_txt.split()[1])
    show_plot_bar(list_date, list_speed, list_gust)


def main(city_name: str, command: str, indicator: str) -> None:
    match command:
        case "weather":
            return get_weather(city_name)
        case "temp":
            return get_temperature(city_name)
        case "temp_plot":
            return get_plot_temperature(city_name, indicator)
        case "wind_plot":
            return get_plot_weather(city_name)


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--name", type=str, default="Moscow", help="City name")
    argparser.add_argument(
        "--com", type=str, default="weather", help="Command", choices=["weather", "temp", "temp_plot", "wind_plot"]
    )
    argparser.add_argument(
        "--ind", type=str, default="temp", help="Indicator", choices=["temp", "feels_like", "pressure", "humidity"]
    )
    args = argparser.parse_args()

    main(args.name, args.com, args.ind)
