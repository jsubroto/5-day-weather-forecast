import requests
import calendar

api_key = '<your_api_key>'
api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key

running = True

print('Welcome to Jaimes Subroto\'s 5 day weather forecast application using OpenWeatherMap\'s API!')

# Program loop
while running:

    # Asks the user for the city or zip code to be queried
    while True:

        # Input validation
        try:
            print('\nThis application supports search by city(0) or search by zip code(1).')
            search = int(input('Please input 0 or 1: '))
        except ValueError:
            print("Sorry, I didn't understand that.")
        else:
            # Passed the validation test

            if search == 0:
                city = input('Please input the city name: ')
                if city.lower() == 'sf':
                    city = 'San Francisco, US'

                # Appends the city to the api call
                api_call += '&q=' + city
                break
                
            elif search == 1:
                zip_code = input('Please input the zip code: ')
                
                # Appends the zip code to the api call
                api_call += '&zip=' + zip_code
                break
                
            else:
                # Prints the invalid number (not 0 or 1)
                print('{} is not a valid option.'.format(search))

    # Stores the Json response
    json_data = requests.get(api_call).json()

    # Print number of lines returned by this API call
    # print(json_data['cnt'])

    location_data = {
        'city': json_data['city']['name'],
        'country': json_data['city']['country']
    }

    # Prints the city, country
    print('\n{city}, {country}'.format(**location_data))

    # The current date we are iterating through
    current_date = ''

    # Iterates through the array of dictionaries named list
    for item in json_data['list']:

        # Time of the weather data received partitioned into 3 hour blocks
        time = item['dt_txt']

        # Split the time into date and hour (Ex: 2018-04-15 06:00:00)
        next_date, hour = time.split(' ')

        # Stores the current date and prints it once
        if current_date != next_date:
            current_date = next_date
            year, month, day = current_date.split('-')
            date = {'y': year, 'm': month, 'd': day}
            print('\n{m}/{d}/{y}'.format(**date))
        
        # Grabs the first 2 integers from our HH:MM:SS string to get the hours
        hour = int(hour[:2])

        # AM (ante meridiem) and PM (post meridiem)
        if hour < 12:
            if hour == 0:
                hour = 12
            meridiem = 'AM'
        else:
            if hour > 12:
                hour -= 12
            meridiem = 'PM'

        # Prints the hours HH:MM AM/PM
        print('\n%i:00 %s' % (hour, meridiem))

        # Temperature is measured Kelvin
        temperature = item['main']['temp']

        # Weather condition
        description = item['weather'][0]['description'],

        # Prints the description as well as the temperature in Celcius and Farenheit
        print('Weather condition: %s' % description)
        print('Celcius: {:.2f}'.format(temperature - 273.15))
        print('Farenheit: %.2f' % (temperature * 9/5 - 459.67))

    # Prints the calendar of the current month
    calendar = calendar.month(int(year), int(month))
    print('\n'+ calendar)

    # Asks user if he/she wants to exit
    while True:
        running = input('Anything else we can help you with? ')
        if running.lower() == 'yes' or running.lower() == 'y':
            print('Great!')
            break
        elif running.lower() == 'no' or running.lower() == 'n' or running == 'exit':
            print('Thank you for using Jaimes Subroto\'s 5 day weather forecast application.')
            print('Have a great day!')
            running = False
            break
        else:
            print('Sorry, I didn\'t get that.')