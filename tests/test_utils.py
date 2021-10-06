import unittest
import json
import sys
sys.path.append("..")
from utils import validate_arguments # Rest of functions dont need testing with unit test

""" Tests for the GetWeatherStatistics class functions """

class TestWeatherAPI(unittest.TestCase):

    def test_valid_args(self):
        self.assertRaises(SystemExit, validate_arguments, "invalidArg", "doesnt_exist/alsoInvalid")

if __name__ == '__main__':
    unittest.main()
