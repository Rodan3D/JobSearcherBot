import requests
from logger import logger


class HH_API:
    @logger.catch
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "text": "Empty",
            "area": 113,
            "only_with_salary": True,
            "per_page": 10,
            "page": 0,
        }

    @logger.catch
    def update_keyword(self, new_keyword):
        self.params["text"] = new_keyword

    @logger.catch
    def exclude_keyword(self, keyword_to_exclude):
        if "text" in self.params and self.params["text"]:
            self.params["text"] += f" -{keyword_to_exclude}"
        else:
            self.params["text"] = f"-{keyword_to_exclude}"

    @logger.catch
    def search_vacancies(self):
        response = requests.get(self.url, params=self.params)

        if response.status_code == 200:
            vacancies_data = response.json()
            return vacancies_data["items"]
        else:
            print("Ошибка при запросе:", response.status_code)
            return []


if __name__ == "__main__":
    hh_api = HH_API()
    hh_api.search_vacancies()
