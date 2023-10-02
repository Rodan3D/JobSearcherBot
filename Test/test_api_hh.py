import unittest
from unittest.mock import patch

from api_hh import HH_API


class TestHHAPI(unittest.TestCase):
    def setUp(self):
        self.hh_api = HH_API()

    def test_input_keyword(self):
        self.hh_api.input_keyword("python")
        self.assertEqual(self.hh_api.params["text"], "python")

    @patch("api_hh.city_info.search_and_print_city_code")
    def test_input_area(self, mock_search_city_code):
        mock_search_city_code.return_value = "city_code"
        self.hh_api.input_area("Moscow")
        self.assertEqual(self.hh_api.params["area"], "city_code")

    def test_exclude_keywords(self):
        self.hh_api.params["text"] = "developer"
        self.hh_api.exclude_keywords("java, javascript")
        self.assertEqual(
            self.hh_api.params["text"], "developer NOT java NOT javascript"
        )

    @patch("api_hh.requests.get")
    def test_search_vacancies_successful(self, mock_requests_get):
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"title": "Job 1"}, {"title": "Job 2"}]
        }

        vacancies = self.hh_api.search_vacancies()
        self.assertEqual(len(vacancies), 2)

    @patch("api_hh.requests.get")
    def test_search_vacancies_failed(self, mock_requests_get):
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 404

        vacancies = self.hh_api.search_vacancies()
        self.assertEqual(len(vacancies), 0)

    def test_format_salary(self):
        salary_data = {"from": 3000, "to": 5000, "currency": "RUB"}
        formatted_salary = self.hh_api.format_salary(salary_data)
        self.assertEqual(formatted_salary, "3000 - 5000 RUB")


if __name__ == "__main__":
    unittest.main()
