import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в формате: \n <имя валюты, цену которой хотите узнать> \
<имя валюты в которой надо узнать цену первой валюты> <количество переводимой валюты> \
\nНапример: евро рубль 10 - перевести 10 евро в рубли\
\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступны валюты:'
    for key, value in keys.items():
        text = '\n'.join((text, key + ' (' + value + ')',))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        convert_values = message.text.lower().split(' ')
        if len(convert_values) > 3:
            raise ConvertionException('Слишком много параметров.')
        if len(convert_values) < 3:
            raise ConvertionException('Слишком мало параметров.')

        quote, base, amount = convert_values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

