# import libraries
import json
import os
import requests
import statistics
from utils import validate_arguments, get_arguments, answers_to_json_file
from operator import itemgetter

"""
Questions:
    1: "1. What will the temperature be in Bath at 10am on Wednesday morning?",
    2: "2. Does the pressure fall below 1000 millibars in Edinburgh at any time on Friday?",
    3: "3. What is the median temperature during the week for Cardiff?",
    4: "4. In which city is the highest wind speed recorded this week? If there is more than one city shares the maximum speed, choose the one which is first alphabetically.",
    5: "5. It is likely to snow if there is precipitation when the temperature is below 2 degrees. Will it snow in any of the cities this week?" }
"""

# Call API and return list of all available cities
def get_list_of_cities():
    url = "http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/cities/"
    json_cities = requests.get(url).json()
    list_of_cities = [i for i in json_cities["cities"]] # JSON object to Python list
    return list_of_cities

# Initalise class with city
class City:
    def __init__(self, city, API_id):
        self.city = city
        self.url = (f"http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/{API_id}/{city}/")
        self.json_data = requests.get(self.url).json()
    def get_list_of_all_vals_in_week(self, weather_stat): # Returns all values of a certain weather statistic in a week. Saves iterating through days.
        weather_stat_list = [[hour[weather_stat] for hour in self.json_data[day]] for day in self.json_data]
        joined_weather_stat_list = [item for list in weather_stat_list for item in list]
        return joined_weather_stat_list

# Weather statistics used to answer questions about a city
class GetWeatherStatistics(City):
    def temp_at_time(self, day, time): # Return int
        temperature = self.json_data[day][time-1]["temperature"]
        return int(temperature)
    def pressure_below(self, day, is_below): # Return bool
        pressure_below_1000_milibars = False
        for item in self.json_data[day]:
            if item["pressure"] < is_below:
                pressure_below_1000_milibars = True
                return pressure_below_1000_milibars
            else:
                pass
        return pressure_below_1000_milibars
    def median_temperature(self): # Return int
        weekly_temps = self.get_list_of_all_vals_in_week("temperature")
        return int(statistics.median(weekly_temps))
    def snow(self): # Return bool
        snow = False
        for day in self.json_data:
            for hour in self.json_data[day]:
                if hour["precipitation"] > 0 and hour["temperature"] < 2:
                    snow = True
                    return snow
                else:
                    pass
        return snow
    def highest_windspeed(self): # Return int
        weekly_wind_speeds = self.get_list_of_all_vals_in_week("wind_speed")
        return max(weekly_wind_speeds)

class AllCityStatistics:
    def __init__(self, cities_dictonary):
        self.cities = cities_dictonary # dictonary of cities
    def snow_this_week(self): # Will it snow in any of the cities this week? return bool
        for city in self.cities.values():
            if city.snow():
                return True
            else:
                pass
        return False
    def highest_windspeed_this_week(self): # Return highest windspeed of all cities this week
        highest_windspeed_per_city = [[i.highest_windspeed(), i.city] for i in self.cities.values()]
        max_wind_speed = sorted(highest_windspeed_per_city, key=itemgetter(0))[-1][0]
        cities_with_max_wind_speed = [i for i in highest_windspeed_per_city if i[0] == max_wind_speed]
        cities_with_max_wind_speed_sorted = sorted(cities_with_max_wind_speed, key=itemgetter(1))
        city_max_wind_speed = cities_with_max_wind_speed_sorted[0][1]
        return city_max_wind_speed

def main(API_id, file_path):
    city_classes = {}
    answers = []

    # Initalise dictonary consisting of a class for each city
    cities = get_list_of_cities()
    for city in cities:
        city_classes[city] = GetWeatherStatistics(city, API_id)

    # Initalise class of all cities for the questions involving multiple cities. Last two questions.
    all_cities = AllCityStatistics(city_classes)

    # Get answers to questions and append answers of the questions to a list for saving in a JSON list in a file location as specified
    answers.append(city_classes["bath"].temp_at_time("wednesday", 10))
    answers.append(city_classes["edinburgh"].pressure_below("friday", 1000))
    answers.append(city_classes["cardiff"].median_temperature())
    answers.append(all_cities.highest_windspeed_this_week())
    answers.append(all_cities.snow_this_week())

    # Save answers to file
    answers_to_json_file(answers, file_path)

if __name__ == '__main__':
    API_id, file_path = get_arguments()
    validate_arguments(API_id, file_path) # Check args are valid before preceding
    main(API_id, file_path)
