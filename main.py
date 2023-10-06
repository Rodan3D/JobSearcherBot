from bot import bot

# Запуск бота
if __name__ == '__main__':
    print('Я запущен!')
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            pass
