import telebot
from functional import *


TOKEN = '5594580495:AAFZ6mg09OahJq-P7HrUEGSzONm4lRtEmxk'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    mess = 'Привет, жду ссылку на трансляцию!'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def main(message):
    try:
        if message.text[:8] == 'https://':
            bot.send_message(message.chat.id, 'Сейчас все сделаю')

            pres_link = get_links(message, bot, get_html(message.text))

            if pres_link is not None:
                count_slides = download_slides(url=pres_link)

                make_zip(count_slides)

                send_pres(message, bot)

                remove()
        else:
            bot.send_message(message.chat.id, 'Ссылка невалидна, попробуй отправить ее с протоколом https:')

    except Exception as ex:
        mess = f'Чувак, я сдох. Вот ссылка: @{message.from_user.username}\nВот ошибка: {ex}'
        adm_1 = '1374749814'
        adm_2 = '243807051'
        bot.send_message(adm_2, mess)
        bot.send_message(adm_1, mess)
        print(ex)

    finally:
        pass


if __name__ == '__main__':
    bot.infinity_polling()