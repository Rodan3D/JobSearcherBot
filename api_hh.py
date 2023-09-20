import requests


class HH_API:
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.params = {
            "text": "",
            "area": 113,
            "only_with_salary": True,
            "per_page": 10,
            "page": 0,
        }

    def update_keyword(self, new_keyword):
        self.params["text"] = new_keyword

    def search_vacancies(self):
        response = requests.get(self.url, params=self.params)

        if response.status_code == 200:
            vacancies_data = response.json()
            return vacancies_data["items"]
        else:
            print("Ошибка при запросе:", response.status_code)
            return []

    # def search_by_keyword(self, keyword):
    #     self.update_keyword(keyword)
    #     return self.search_vacancies()


if __name__ == "__main__":
    hh_api = HH_API()
    hh_api.search_vacancies()
