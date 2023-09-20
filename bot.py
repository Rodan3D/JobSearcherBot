import telebot
from loguru import logger
from telebot import types

from api_hh import HH_API
from config import TELEGRAM_TOKEN

# Замените 'TELEGRAM_TOKEN' на ваш токен Telegram бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Логирование
logger.add(
    "debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 MB",
    compression="zip",
)
#
# Создайте экземпляр HH_API
hh_api = HH_API()


@logger.catch
def create_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    item_help = types.KeyboardButton("Помощь 🆘")
    item_search = types.KeyboardButton("Меню настройки вакансий ⚙️")
    item_info = types.KeyboardButton("Информация ℹ️")
    markup.add(item_help, item_search, item_info)
    return markup


@logger.catch
@bot.message_handler(commands=["start"])
def start(message):
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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_change_key = types.KeyboardButton("Изменить ключевое слово 🔄")
    item_exclude_word = types.KeyboardButton("Слова-исключения")
    item_search_vacancy = types.KeyboardButton("Поиск вакансий 🔎")
    item_back = types.KeyboardButton("Назад ↩️")
    markup.add(item_change_key, item_exclude_word, item_search_vacancy, item_back)
    bot.send_message(
        message.chat.id, "Вы перешли в Меню настройки вакансий 🔎", reply_markup=markup
    )


@bot.message_handler(
    func=lambda message: message.text == "Поиск вакансий 🔎" or message.text == "/search"
)
@logger.catch
def search_command(message):
    try:
        vacancies = hh_api.search_vacancies()
        if vacancies:
            response = "Результаты поиска вакансий:\n\n"
            for vacancy in vacancies:
                response += f"Название вакансии: {vacancy['name']}\n"
                response += f"Зарплата: {vacancy['salary']}\n"
                response += f"Ссылка на вакансию: {vacancy['alternate_url']}\n"
                response += "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Ничего не найдено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Изменить ключевое слово 🔄"
    or message.text == "/key"
)
def change_keyword(message):
    bot.send_message(
        message.chat.id, "Введите новое ключевое слово для поиска вакансий:"
    )
    bot.register_next_step_handler(message, set_new_keyword)


@logger.catch
def set_new_keyword(message):
    new_keyword = message.text
    hh_api.update_keyword(new_keyword)
    bot.send_message(
        message.chat.id, f"Новое ключевое слово для поиска вакансий: {new_keyword}"
    )


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Помощь 🆘" or message.text == "/help"
)
def help_bot(message):
    bot.send_message(
        message.chat.id,
        "/start - начать диалог с ботом\n"
        "/help  - выводит все команды бота\n"
        "/vacancy_search - поиск вакансий\n"
        "/info - информация",
    )


@logger.catch
@bot.message_handler(
    func=lambda message: message.text == "Информация ℹ️" or message.text == "/info"
)
def about_info(message):
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
    bot.send_message(
        message.chat.id,
        'Я бот-настройщик по "узкому" поиску вакансий на сайте HeadHunter. Под '
        '"узким" понимается без всякого лишнего мусора',
    )


@logger.catch
@bot.message_handler(func=lambda message: message.text == "Контакты 📞")
def contacts_info(message):
    bot.send_message(message.chat.id, "Связь с разработчиком : https://t.me/Rodan3D")


@logger.catch
@bot.message_handler(func=lambda message: message.text == "Назад ↩️")
def back(message):
    markup = create_markup()
    bot.send_message(
        message.chat.id, "Вы вернулись в главное меню", reply_markup=markup
    )


@logger.catch
@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(
        message.chat.id,
        "Извините, я не понял ваш запрос 🤷‍♂️. Для получения списка команд воспользуйтесь командой /start или "
        "нажмите на"
        'кнопку "Помощь 🆘"',
    )


# Запуск бота
if __name__ == "__main__":
    print("Я запущен!")
    bot.polling(none_stop=True)
