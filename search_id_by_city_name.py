"""
Модуль CityData предоставляет класс для работы с данными о городах и
их кодах, а также функциональность по поиску кода города по его имени.
"""
import difflib
from typing import Optional

from logger import logger

FILE_PATH = 'city_codes.txt'


class CityData:
    """
    Класс CityData предоставляет функциональность для работы с данными
    о городах и их кодах.

    Args:
         Словарь, содержащий данные о городах и соответствующих им кодах.
    """

    @logger.catch
    def __init__(self, FILE_PATH: str) -> None:
        """
        Инициализирует объект CityData.

        Args:
            FILE_PATH (str): Путь к файлу с данными о городах и кодах.
        """
        self.city_data = {}
        self.load_data(FILE_PATH)

    @logger.catch
    def load_data(self, FILE_PATH: str) -> None:
        """
        Загружает данные о городах и кодах из файла и создает словарь
        city_data.

        Args:
           FILE_PATH (str): Путь к файлу с данными о городах и кодах.
        """
        try:
            with open(FILE_PATH, 'r') as file:
                document_text = file.read()
                lines = document_text.split('\n')
                for line in lines:
                    if 'Город:' in line and 'Код города:' in line:
                        city_name = line.split(
                            'Город:')[1].split(';')[0].strip()
                        city_code = line.split('Код города:')[1].strip()
                        city_name = city_name.strip()
                        self.city_data[city_name] = city_code
        except FileNotFoundError:
            print(f'Файл {FILE_PATH} не найден.')

    @logger.catch
    def find_city_code(self, search_city: str) -> Optional[str]:
        """
        Находит код города по его имени.

        Args:
           search_city (str): Название города.

        Returns:
           Optional[str]: Код города, если город найден;
           в противном случае None.
        """
        if search_city in self.city_data:
            return self.city_data[search_city]

        closest_matches = difflib.get_close_matches(
            search_city, self.city_data.keys(), n=1
        )
        if closest_matches:
            closest_match = closest_matches[0]
            return self.city_data[closest_match]

    @logger.catch
    def search_and_print_city_code(self, search_city: str) -> Optional[str]:
        """
        Поиск кода города и вывод результата.

        Args:
            search_city (str): Название города.

        Returns:
            Optional[str]: Код города, если город найден;
            в противном случае None.

        """
        city_code = self.find_city_code(search_city)
        if city_code:
            return city_code
        print(f'Город {search_city} не найден.')


if __name__ == '__main__':
    city_info = CityData(FILE_PATH)
    search_city = input('Введите название города: ')
    city_info.search_and_print_city_code(search_city)
