import requests
import calendar
from collections import defaultdict

api_key = "<your_api_key>"
api_call = "https://api.openweathermap.org/data/2.5/forecast?appid=" + api_key
invalid_input_message = "Sorry, I didn't get that."

print("Welcome to Jaimes Subroto's 5 day weather forecast application using the OpenWeatherMap Weather API!")
if api_key == "<your_api_key>":
    print("Please provide your OpenWeatherMap API key.")
    exit()


def get_city_or_zip_code():
    while True:
        try:
            print("\nThis application supports search by city(0) or by zip code(1).")
            search = int(input("Please input 0 or 1: "))
        except ValueError:
            print(invalid_input_message)
        else:

            if search == 0:
                city = input("Please input the city name: ")
                if city.lower() == "sf":
                    city = "San Francisco, US"
                return "&q=" + city

            elif search == 1:
                zip_code = input("Please input the zip code: ")
                return "&zip=" + zip_code

            else:
                # Prints the invalid number (not 0 or 1)
                print("{} is not a valid option.".format(search))


is_running = True
while is_running:

    # Stores the Json response
    json_data = requests.get(api_call + get_city_or_zip_code()).json()

    location_data = {
        "city": json_data["city"]["name"],
        "country": json_data["city"]["country"]
    }

    print("\n{city}, {country}".format(**location_data))

    grouped_data = defaultdict(list)

    # Iterates through the array of dictionaries named list in json_data
    for item in json_data["list"]:

        # Time of the weather data received, partitioned into 3 hour blocks
        time = item["dt_txt"]

        # Split the time into date and hour [YYYY-MM-DD 06:00:00]
        date, hour = time.split(' ')

        # Stores the current date and prints it once
        year, month, day = date.split('-')
        date = f"{month}/{day}/{year}"

        # Grabs the first 2 characters from our HH:MM:SS string to get the hours
        hour = int(hour[:2])

        # Sets the AM (ante meridiem) or PM (post meridiem) period
        meridiem = "AM" if hour < 12 else "PM"
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12

        # Formatted as [HH:MM AM/PM]
        time = f"{hour}:00 {meridiem}"

        # Temperature is measured in Kelvin
        temperature = item["main"]["temp"]

        # Weather conditions
        description = item["weather"][0]["description"]
        humidity = item["main"]["humidity"]
        grouped_data[date].append((time, temperature, description, humidity))

    for date in grouped_data:
        print("\n" + date)
        for time, temperature, description, humidity in grouped_data[date]:
            print("\n" + time)
            print("Weather condition: %s" % description)
            print(f"Humidity: {humidity}%")
            print("Celcius: {:.2f}".format(temperature - 273.15))
            print("Fahrenheit: %.2f" % ((temperature - 273.15) * 9/5 + 32))

    # Prints a calendar of the current month
    calendar_month = calendar.month(int(year), int(month))
    print('\n' + calendar_month)

    # Asks the user if he/she wants to exit
    while True:
        continue_input = input("Anything else we can help you with? ")
        if continue_input.lower() in {"yes", 'y'}:
            print("Great!")
            break
        elif continue_input.lower() in {"no", 'n', "exit"}:
            print(
                "Thank you for using Jaimes Subroto's 5 day weather forecast application.")
            print("Have a great day!")
            is_running = False
            break
        else:
            print(invalid_input_message)
