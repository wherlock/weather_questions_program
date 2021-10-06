import unittest
from load_json import load_json_file
import sys
sys.path.append("../src/")
from answer_weather_questions import GetWeatherStatistics

""" Tests for the GetWeatherStatistics class functions """

class TestWeatherAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        test_json = load_json_file("./test_data/example_json.json")
        self.city = GetWeatherStatistics("bristol", 2)
        self.city.json_data = test_json

    def test_median_temp(self):
        self.assertEqual(self.city.median_temperature(), 5)

    def test_pressure_below(self):
        self.assertTrue(self.city.pressure_below("monday", 500000))
        self.assertFalse(self.city.pressure_below("monday", 1))

    def test_temp_at_time(self):
        self.assertEqual(self.city.temp_at_time("monday", 2), 6)

    def test_snow(self):
        self.assertFalse(self.city.snow())

    def test_highest_windspeed(self):
        self.assertEqual(self.city.highest_windspeed(), 12)

if __name__ == '__main__':
    unittest.main()
