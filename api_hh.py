"""
Модуль, реализующий взаимодействие с API hh.ru.
"""

from typing import Dict, Union

import requests

from add_key_and_exclude_words import add_excluded_word_stat, add_keyword_stat
from logger import logger
from search_id_by_city_name import CityData

city_info = CityData('city_codes.txt')


class HH_API:
    """
    Класс для взаимодействия с API hh.ru и поиска вакансий.
    """
    @logger.catch
    def __init__(self) -> None:
        self.url = 'https://api.hh.ru/vacancies'
        self.params: Dict[str, Union[str, int, bool]] = {
            'text': '',
            'area': '',
            'only_with_salary': True,
            'per_page': 30,
            'page': 1,
        }

    @logger.catch
    def input_keyword(self, new_keyword: str) -> None:
        """
        Устанавливает ключевое слово для поиска вакансий.

        Args:
            new_keyword: Строка с ключевым словом.
        """
        self.params['text'] = new_keyword
        add_keyword_stat(new_keyword, 1)

    @logger.catch
    def input_area(self, city: str) -> None:
        """
        Устанавливает область (город) для поиска вакансий.

        Args:
            city: Строка с названием города.
        """
        city_code = city_info.search_and_print_city_code(city)
        if city_code:
            self.params['area'] = city_code

    @logger.catch
    def exclude_keywords(self, keywords_to_exclude: str) -> None:
        """
        Исключает ключевые слова из поиска вакансий.

        Args:
             keywords_to_exclude: Строка с ключевыми словами для исключения.
        """
        keywords_list = keywords_to_exclude.split(',')
        keywords_list = [keyword.strip() for keyword in keywords_list]

        if 'text' in self.params and self.params['text']:
            self.params['text'] += f" NOT {' NOT '.join(keywords_list)}"
        else:
            self.params['text'] = f"NOT {' NOT '.join(keywords_list)}"

        for keyword_to_exclude in keywords_list:
            add_excluded_word_stat(keyword_to_exclude, 1)

    @logger.catch
    def search_vacancies(self) -> list:
        """
        Осуществляет поиск вакансий с заданными параметрами.

        Returns:
            Список словарей с информацией о вакансиях.
        """
        response = requests.get(self.url, params=self.params)

        if response.status_code == 200:
            vacancies_data = response.json()
            return vacancies_data['items']

        print('Ошибка при запросе:', response.status_code)
        return []

    @logger.catch
    def format_salary(self, salary_data: Dict[str, Union[
        int, None, str]]) -> str:
        """
        Форматирует информацию о зарплате из словаря в строку.

        Args:
            salary_data: Словарь с данными о зарплате.
        Returns:
            format_salary: Строка с отформатированной информацией о зарплате.
        """
        formatted_salary = ''
        if 'from' in salary_data and salary_data['from'] is not None:
            formatted_salary += str(salary_data['from'])
        if 'to' in salary_data and salary_data['to'] is not None:
            if 'from' in salary_data and salary_data['from'] is not None:
                formatted_salary += f" - {salary_data['to']}"
            else:
                formatted_salary += str(salary_data['to'])
        formatted_salary += f" {salary_data['currency']}"
        return formatted_salary


if __name__ == '__main__':
    hh_api = HH_API()
    hh_api.search_vacancies()
