import telebot # импорт библиотеки для Telegram-ботов

import extension as e # импорт файла 'extension.py' с классами ошибок
from config import TOKEN # импорт токена из файла 'config.py'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands= ['start', 'help']) # функция ответа на сообщения /start и /help
def start_help(message: telebot.types.Message):
    text = 'Чтобы перевести валюту введите комманду в слудющем формате:\n<имя валюты> \
<в какую валюту перевести>\
<количество переводимой валюты>\n\
Пример:\n доллар рубль 100\n\
Посмотреть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands= ['values']) # с поощью команды /values выводит список доступных валют
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in e.keys:
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types= ['text']) # главная функция работы бота
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise e.APIException('Некорректые параметры, введите корректный запрос.')
            
        quote, base, amount = values
        total_base = e.CurrencyConverter.get_price(quote, base, amount)
    except e.APIException as n:
        bot.reply_to(message, f'Ошибка пользователя:\n{n}')
    except Exception as n:
        bot.reply_to(message, f'Не удалось обработать команду:\n{n}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(non_stop=True)