import unittest
from load_json import load_json_file
import sys
sys.path.append("../src/")
from answer_weather_questions import AllCityStatistics, GetWeatherStatistics

""" Tests for the AllCityStatistics class functions """

class TestWeatherAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Create dictonary out of example city files for testing
        bristol = GetWeatherStatistics("bristol", 2)
        bristol.json_data = load_json_file("./test_data/example_json.json")
        bath = GetWeatherStatistics("bath", 2)
        bath.json_data = load_json_file("./test_data/example_json1.json")
        # Create dictonary for testing the class
        city_dictonary = {}
        city_dictonary["bristol"] = bristol
        city_dictonary["bath"] = bath
        self.all_cities = AllCityStatistics(city_dictonary)

    def test_snow_this_week(self):
        self.assertTrue(self.all_cities.snow_this_week())

    def test_highest_windspeed_this_week(self):
        self.assertEqual(self.all_cities.highest_windspeed_this_week(), "bath")

if __name__ == '__main__':
    unittest.main()
