import os
import sys

import requests

APP_NAME = "Jaimes Subroto's 5-day weather forecast application"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"
INVALID = "Sorry, I didn't get that."

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    print("Missing OPENWEATHER_API_KEY. Set it in your .env.")
    sys.exit(1)


def goodbye():
    print(f"Thank you for using {APP_NAME}.")
    print("Have a great day!")


def get_query_param():
    while True:
        try:
            choice = int(input("\nSearch by city(0) or zip(1): "))
        except ValueError:
            print(INVALID)
            continue
        if choice == 0:
            cities = {"sf": "San Francisco", "la": "Los Angeles"}
            city = input("City name: ").strip().lower()
            city = cities.get(city, city)
            return {"q": city}
        if choice == 1:
            return {"zip": input("Zip code: ")}
        print(f"{choice} is not a valid option.")


def fetch_forecast(params):
    params.update({"appid": API_KEY, "units": "metric"})
    try:
        r = requests.get(BASE_URL, params=params, timeout=15)
        if r.status_code == 401:
            print("Got a 401 response. Check OPENWEATHER_API_KEY in your .env.")
            goodbye()
            sys.exit(1)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Request failed: {e}")
        goodbye()
        sys.exit(1)


def main():
    print(f"Welcome to {APP_NAME} using the OpenWeatherMap API!")
    while True:
        data = fetch_forecast(get_query_param())
        print(f"\n{data['city']['name']}, {data['city']['country']}")

        for item in data["list"]:
            temp = item["main"]["temp"]
            humidity = item["main"]["humidity"]
            desc = item["weather"][0]["description"].capitalize()
            print(
                f"{item['dt_txt'][:-3]} UTC\n"
                f"Weather condition: {desc}\n"
                f"Humidity: {humidity}%\n"
                f"Celsius: {temp:.2f}\n"
                f"Fahrenheit: {(temp * 9 / 5 + 32):.2f}\n"
            )

        while True:
            match input("Anything else we can help you with? (y/n) ").strip().lower():
                case "y" | "yes":
                    print("Great!")
                    break
                case "n" | "no" | "exit":
                    goodbye()
                    return
                case _:
                    print(INVALID)


if __name__ == "__main__":
    main()
