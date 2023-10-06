"""
Модуль, реализующий создание клавиатуры в Telegram боте.
"""
from telebot import types
from logger import logger


class KeyboardHandler:
    """
    Класс, предназначенный для управления клавиатурой и меню в Telegram боте.
    """
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    @logger.catch
    def create_markup() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        item_help = types.KeyboardButton("Помощь 🆘")
        item_search = types.KeyboardButton("Меню настройки вакансий ⚙️")
        item_info = types.KeyboardButton("Информация ℹ️")
        markup.add(item_help, item_search, item_info)
        return markup

    @logger.catch
    def start(self, message):
        markup = self.create_markup()
        self.bot.send_message(
            message.chat.id,
            "Привет, {0.first_name}!".format(message.from_user),
            reply_markup=markup,
        )

    @logger.catch
    def search(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_input_keyword = types.KeyboardButton("Ввести ключевое слово")
        item_search_vacancy = types.KeyboardButton("Поиск 🔎")
        item_exclude_word = types.KeyboardButton("Добавить слово-исключение")
        item_popular_keywords = types.KeyboardButton("Популярные " 
                                                     "ключевые слова")
        item_popular_excluded_words = types.KeyboardButton(
            "Популярные слова-исключения"
        )
        item_back = types.KeyboardButton("Назад ↩️")
        markup.add(
            item_input_keyword,
            item_search_vacancy,
            item_exclude_word,
            item_popular_keywords,
            item_popular_excluded_words,
            item_back,
        )
        self.bot.send_message(
            message.chat.id,
            "Вы перешли в Меню настройки вакансий 🔎",
            reply_markup=markup,
        )

    @logger.catch
    def info(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item_about = types.KeyboardButton("О боте 💾")
        item_contact = types.KeyboardButton("Контакты 📞")
        item_back = types.KeyboardButton("Назад ↩️")
        markup.add(item_about, item_contact, item_back)
        self.bot.send_message(
            message.chat.id, "Вы перешли в меню Информация ℹ️",
            reply_markup=markup
        )

    def back(self, message):
        markup = self.create_markup()
        self.bot.send_message(
            message.chat.id, 'Вы вернулись в главное меню',
            reply_markup=markup
        )


if __name__ == "__main__":
    keyboard_handler = KeyboardHandler
