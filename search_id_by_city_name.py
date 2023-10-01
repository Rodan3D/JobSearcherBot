import difflib

from logger import logger


class CityData:
    @logger.catch
    def __init__(self, file_path):
        self.city_data = {}
        self.load_data(file_path)

    @logger.catch
    def load_data(self, file_path):
        try:
            with open(file_path, "r") as file:
                document_text = file.read()
                lines = document_text.split("\n")
                for line in lines:
                    if "Город:" in line and "Код города:" in line:
                        city_name = line.split("Город:")[1].split(";")[0].strip()
                        city_code = line.split("Код города:")[1].strip()
                        city_name = city_name.strip()
                        self.city_data[city_name] = city_code
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")

    @logger.catch
    def find_city_code(self, search_city):
        if search_city in self.city_data:
            return self.city_data[search_city]
        else:
            # Попробуйте найти наиболее подходящее совпадение среди городов
            closest_matches = difflib.get_close_matches(
                search_city, self.city_data.keys(), n=1
            )
            if closest_matches:
                closest_match = closest_matches[0]
                return self.city_data[closest_match]
            else:
                return None

    @logger.catch
    def search_and_print_city_code(self, search_city):
        city_code = self.find_city_code(search_city)
        if city_code:
            # Возвращаем обновленное значение area_param
            return city_code
        else:
            print(f"Город {search_city} не найден.")
            # Возвращаем None, если город не найден
            return None


if __name__ == "__main__":
    file_path = "city_codes.txt"
    city_info = CityData(file_path)
    search_city = input("Введите название города: ")
    city_info.search_and_print_city_code(search_city)
