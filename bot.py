import telebot
from telebot import types

from add_key_and_exclude_words import (
    get_popular_excluded_words_from_database,
    get_popular_keywords_from_database,
)
from api_hh import HH_API
from config import TELEGRAM_TOKEN
from logger import logger

# Замените 'TELEGRAM_TOKEN' на ваш токен Telegram бота в файле config.py
bot = telebot.TeleBot(TELEGRAM_TOKEN)
# Создали экземпляр HH_API
hh_api = HH_API()
# Создаем состояние ожидания ключевого слова для поиска
waiting_for_keyword = {}
# Создаем состояние ожидания города для поиска
waiting_for_city = {}


@logger.catch
def create_markup():
    """
    Создает и возвращает разметку клавиатуры для бота.

    Returns:
       types.ReplyKeyboardMarkup: Разметка клавиатуры.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    item_help = types.KeyboardButton("Помощь 🆘")
    item_search = types.KeyboardButton("Меню настройки вакансий ⚙️")
    item_info = types.KeyboardButton("Информация ℹ️")
    markup.add(item_help, item_search, item_info)
    return markup


@logger.catch
@bot.message_handler(commands=["start"])
def start(message):
    """
    Обработчик команды /start для начала диалога с ботом.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    markup = create_markup()
    bot.send_message(
        message.chat.id,
        "Привет, {0.first_name}!".format(message.from_user),
        reply_markup=markup,
    )


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Меню настройки вакансий ⚙️"
    or message.text == "/main"
)
def search(message):
    """
    Обработчик команды "Меню настройки вакансий ⚙️" для перехода в меню настройки.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_input_keyword = types.KeyboardButton("Ввести ключевое слово")
    item_search_vacancy = types.KeyboardButton("Поиск 🔎")
    item_exclude_word = types.KeyboardButton("Добавить слово-исключение")
    item_popular_keywords = types.KeyboardButton("Популярные ключевые слова")
    item_popular_excluded_words = types.KeyboardButton("Популярные слова-исключения")
    item_back = types.KeyboardButton("Назад ↩️")
    markup.add(
        item_input_keyword,
        item_search_vacancy,
        item_exclude_word,
        item_popular_keywords,
        item_popular_excluded_words,
        item_back,
    )
    bot.send_message(
        message.chat.id, "Вы перешли в Меню настройки вакансий 🔎", reply_markup=markup
    )


@bot.message_handler(
    func=lambda message: message.text == "Поиск 🔎" or message.text == "/search"
)
@logger.catch
def search_command(message):
    """
    Обработчик команды "Поиск 🔎" для выполнения поиска вакансий.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    try:
        vacancies = hh_api.search_vacancies()
        if vacancies:
            response = "Результаты поиска вакансий:\n\n"
            for vacancy in vacancies:
                response += f"{vacancy['name']}\n"
                response += f"Зарплата: {hh_api.format_salary(vacancy['salary'])}\n"
                response += f"Город: {(vacancy['area']['name'])}\n"
                response += f"{vacancy['alternate_url']}\n\n"
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Ничего не найдено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Ввести ключевое слово"
    or message.text == "/input_key"
)
def input_keyword(message):
    """
    Обработчик команды "Ввести ключевое слово" для ввода ключевого слова.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    bot.send_message(message.chat.id, "Введите ключевое слово для поиска:")
    bot.register_next_step_handler(message, set_new_keyword)
    # Устанавливаем состояние ожидания ключевого слова для пользователя
    waiting_for_keyword[message.chat.id] = True


@logger.catch
def set_new_keyword(message):
    """
    Функция для установки нового ключевого слова для поиска.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    new_keyword = message.text
    hh_api.input_keyword(new_keyword)
    bot.send_message(message.chat.id, f"Ключевое слово для поиска: {new_keyword}")
    # Убираем состояние ожидания ключевого слова
    waiting_for_city[message.chat.id] = False
    # Запускаем функцию для запроса города
    set_city(message)


@logger.catch
def set_city(message):
    """
    Функция для установки города для поиска.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    bot.send_message(message.chat.id, "Введите город для поиска:")
    bot.register_next_step_handler(message, set_new_city)
    # Устанавливаем состояние ожидания города для пользователя
    waiting_for_city[message.chat.id] = True


@logger.catch
def set_new_city(message):
    """
    Подфункция для установки города для поиска.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    city = message.text
    hh_api.input_area(city)
    bot.send_message(message.chat.id, f"Город для поиска: {city}")
    # Убираем состояние ожидания ключевого слова
    waiting_for_keyword[message.chat.id] = False
    # Запускаем поиск сразу после ввода ключевого слова
    search_command(message)


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Популярные ключевые слова"
    or message.text == "/popular_keywords"
)
def popular_keywords(message):
    """
    Обработчик команды для извлечения популярных ключевых слов из базы данных и отправки пользователю

    Args:
       message (telebot.types.Message): Объект сообщения Telegram.

    """
    keywords = get_popular_keywords_from_database()
    if keywords:
        response = "Популярные ключевые слова:\n\n"
        for keyword in keywords[:5]:
            response += f"*{keyword}*\n"
        bot.send_message(message.chat.id, response, parse_mode="MARKDOWN")
    else:
        bot.send_message(message.chat.id, "Нет популярных ключевых слов.")


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Популярные слова-исключения"
    or message.text == "/popular_excluded_words"
)
def popular_excluded_words(message):
    """
    Обработчик команды для извлечения популярных слов-исключений из базы данных и отправки пользователю

    Args:
       message (telebot.types.Message): Объект сообщения Telegram.

    """
    excluded_words = get_popular_excluded_words_from_database()
    if excluded_words:
        response = "Популярные слова-исключения:\n\n"
        for word in excluded_words[:5]:
            response += f"*{word}*\n"
        bot.send_message(message.chat.id, response, parse_mode="MARKDOWN")
    else:
        bot.send_message(message.chat.id, "Нет популярных слов-исключений.")


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Добавить слово-исключение"
    or message.text == "/exclude_key"
)
def add_exclude_words(message):
    """
    Обработчик команды для добавления слова-исключения в базу данных.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    bot.send_message(message.chat.id, "Введите слово-исключение:")
    bot.register_next_step_handler(message, set_exclude_keyword)
    # Устанавливаем состояние ожидания ключевого слова для пользователя
    waiting_for_keyword[message.chat.id] = True


@logger.catch
def set_exclude_keyword(message):
    """
    Функция для установки слова-исключения.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    keyword_to_exclude = message.text
    hh_api.exclude_keywords(keyword_to_exclude)
    bot.send_message(
        message.chat.id, f"Добавлено слово-исключение: {keyword_to_exclude}"
    )
    # Убираем состояние ожидания ключевого слова
    waiting_for_city[message.chat.id] = False
    # Запускаем функцию для запроса города
    set_city(message)


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Помощь 🆘" or message.text == "/help"
)
def help_bot(message):
    """
    Обработчик команды для вывода списка команд и описания бота.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    bot.send_message(
        message.chat.id,
        "`/start` - начать диалог с ботом\n"
        "`/help`  - выводит все команды бота\n"
        "`/main` - меню настройки вакансий\n"
        "`/input_key` - ввести ключевое слово\n"
        "`/exclude_key` - добавить слово-исключение\n"
        "`/popular_keywords` - популярные ключевые слова\n"
        "`/popular_excluded_words` - популярные слова-исключения\n"
        "`/info` - информация",
        parse_mode="MARKDOWN",
    )


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Информация ℹ️" or message.text == "/info"
)
def about_info(message):
    """
    Обработчик команды для вывода информации о боте.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_about = types.KeyboardButton("О боте 💾")
    item_contact = types.KeyboardButton("Контакты 📞")
    item_back = types.KeyboardButton("Назад ↩️")
    markup.add(item_about, item_contact, item_back)
    bot.send_message(
        message.chat.id, "Вы перешли в меню Информация ℹ️", reply_markup=markup
    )


@logger.catch
@bot.message_handler(func=lambda message: message.text == "О боте 💾")
def about_info(message):
    """
    Функция для вывода информации о боте.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    bot.send_message(
        message.chat.id,
        'Я бот-настройщик по "узкому" поиску вакансий на сайте HeadHunter. Под '
        '"узким" понимается без всякого лишнего мусора',
    )


@logger.catch
@bot.message_handler(func=lambda message: message.text == "Контакты 📞")
def contacts_info(message):
    """
    Функция для вывода контактов с разработчиком.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    bot.send_message(message.chat.id, "Связь с разработчиком : https://t.me/Rodan3D")


@logger.catch
@bot.message_handler(func=lambda message: message.text == "Назад ↩️")
def back(message):
    """
    Функция для вовзрата на шаг назад.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    markup = create_markup()
    bot.send_message(
        message.chat.id, "Вы вернулись в главное меню", reply_markup=markup
    )


@logger.catch
@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    """
    Функция для отработки неизвестных команд.

    Args:
        message (telebot.types.Message): Объект сообщения Telegram.

    """
    bot.send_message(
        message.chat.id,
        "Извините, я не понял ваш запрос 🤷‍♂️. Для получения списка команд воспользуйтесь командой /start или "
        "нажмите на"
        'кнопку "Помощь 🆘"',
    )


# Запуск бота
if __name__ == "__main__":
    print("Я запущен!")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            pass
