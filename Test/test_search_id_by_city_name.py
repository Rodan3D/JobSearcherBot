import unittest
from unittest.mock import patch

from search_id_by_city_name import CityData


class TestCityData(unittest.TestCase):
    def setUp(self):
        self.city_info = CityData('city_codes.txt')

    def test_find_city_code_existing_city(self):
        city_code = self.city_info.find_city_code('Москва')
        self.assertEqual(city_code, '1')

    def test_find_city_code_nonexistent_city(self):
        city_code = self.city_info.find_city_code('NonexistentCity')
        self.assertIsNone(city_code)

    def test_search_and_print_city_code_existing_city(self):
        with patch('builtins.input', return_value='Санкт-Петербург'):
            result = self.city_info.search_and_print_city_code(
                'Санкт-Петербург')
        self.assertEqual(result, '2')

    def test_search_and_print_city_code_nonexistent_city(self):
        with patch('builtins.input', return_value='NonexistentCity'):
            result = self.city_info.search_and_print_city_code(
                'NonexistentCity')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
