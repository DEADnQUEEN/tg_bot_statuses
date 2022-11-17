import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

token = '5649922713:AAExu58PHpyaQ0En6P62fdvkufzMnH3V25M'
bot = telebot.TeleBot(token)


def status_texts(message):
    """
    making text of statuses with signals
    :param message: message from user text
    :return: text with list of status
    """

    with open(f'answers.txt', 'r') as answers:
        answers = answers.readlines()
        for i in range(len(answers)):
            answers[i] = answers[i].rstrip('\n')

    text = f'{answers[2]}\n'

    with open(f'user_data/{message.chat.id}.txt', 'r') as reader:
        reader = reader.readlines()
        for i in range(len(reader)):
            reader[i] = reader[i].rstrip('\n')[8:len(reader[i])]
            url = f'https://{reader[i]}'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            if url[0:30] == 'https://steamcommunity.com/id/':
                status = soup.find('div', class_="profile_in_game_header").text
                text += f'\n'
                nickname = soup.find('span', class_='actual_persona_name').text
                if status == 'Currently Offline':
                    text += f'🔴 - Offline - {nickname}'
                elif status == 'Currently Online':
                    text += f'🟢 - Online - {nickname}'
                elif status == 'Currently In-Game':
                    text += f'🟢 - In game - {nickname}'
                else:
                    text += f'{url} - че то другое'
            else:
                status = 'None'
                text += f'\n{reader[i]} - {status}'

    return text


def menu():
    """
    making menu structure to work with bot without keyboard
    :return: menu of markups
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(types.KeyboardButton(text=f'Добавить'),
               types.KeyboardButton(text=f'Удалить'))

    markup.add(types.KeyboardButton(text=f'Статусы'))

    return markup


@bot.callback_query_handler(func=lambda call: True)
def call_backer(call):

    if call.data == 'refresh':
        try:
            text = status_texts(message=call.message)

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='🔄Обновить🔄', callback_data='refresh'))

            bot.edit_message_text(chat_id=call.from_user.id,
                                  message_id=call.message.id,
                                  text=text,
                                  reply_markup=markup)
        except Exception:
            pass

    elif call.data[0:3] == f'del':

        url = call.data[3:len(call.data)]
        text = ''
        with open(f'user_data/{call.from_user.id}.txt', 'r') as texter:
            texter = texter.readlines()
            for i in range(len(texter)):
                texter[i] = texter[i].rstrip('\n')
                if texter[i] != url:
                    text += f'{texter[i]}\n'

        bot.send_message(chat_id=call.from_user.id,
                         text=f'Я удалил эту ссылку - {url}',
                         reply_markup=menu())

        with open(f'user_data/{call.from_user.id}.txt', 'w') as texter:
            texter.write(text)


@bot.message_handler(commands=['start'])
def starter(message):
    text = ''
    with open('Start_message.txt', 'r') as start_message:
        start_message = start_message.readlines()
        for i in range(len(start_message)):
            text += f'{start_message[i]}'

    with open(f'users/{message.chat.id}.txt', 'w') as worker:
        worker.write('')
    with open(f'user_data/{message.chat.id}.txt', 'w') as worker:
        worker.write('')

    markup = menu()
    bot.send_message(chat_id=message.chat.id,
                     text=text,
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def texter(message):
    """
    [Добавить, Удалить, Статусы]
    """

    chek_list = ['Добавить', 'Удалить', 'Статусы']

    del_markups = types.ReplyKeyboardRemove()

    with open(f'answers.txt', 'r') as answers:
        answers = answers.readlines()
        for i in range(len(answers)):
            answers[i] = answers[i].rstrip('\n')

    if message.text in chek_list:

        with open(f'users/{message.chat.id}.txt', 'w') as writer:
            writer.write(message.text)

        if message.text == 'Добавить':
            works = ''
            with open('work_urls.txt', 'r') as work:
                work = work.readlines()
                for i in range(len(work)):
                    work[i] = work[i].rstrip('\n')
                    works += f'- {work[i]}\n'

            bot.send_message(chat_id=message.chat.id,
                             text=f'{answers[0]}\n\n{works}',
                             reply_markup=del_markups)

        elif message.text == 'Удалить':

            markup = types.InlineKeyboardMarkup()

            with open(f'user_data/{message.chat.id}.txt', 'r') as readers:
                readers = readers.readlines()
                for i in range(len(readers)):
                    readers[i] = readers[i].rstrip('\n')
                    markup.add(types.InlineKeyboardButton(text=readers[i], callback_data=f'del{readers[i]}'))

            bot.send_message(chat_id=message.chat.id,
                             text=f'{answers[4]}',
                             reply_markup=markup)

        elif message.text == 'Статусы':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='🔄Обновить🔄', callback_data='refresh'))

            text = status_texts(message=message)

            bot.send_message(chat_id=message.chat.id,
                             text=text,
                             reply_markup=markup)

    else:
        with open(f'users/{message.chat.id}.txt', 'r') as reader:
            reader = reader.read().rstrip('\n')

        if reader == 'Добавить':

            with open('work_urls.txt', 'r') as work_urls:
                work_urls = work_urls.readlines()
                for i in range(len(work_urls)):
                    work_urls[i] = work_urls[i].rstrip('\n')

            work_urls_lenghts = [len(work_urls[i]) for i in range(len(work_urls))]

            for j in range(len(work_urls)):
                if message.text[0:work_urls_lenghts[j]] == work_urls[j]:
                    with open(f'user_data/{message.chat.id}.txt', 'r') as data:
                        data = data.readlines()
                        for i in range(len(data)):
                            data[i] = data[i].rstrip('\n')

                    with open(f'user_data/{message.chat.id}.txt', 'w') as writer:
                        for i in range(len(data)):
                            writer.write(f'{data[i]}\n')
                        writer.write(f'{message.text}\n')

                    bot.send_message(chat_id=message.chat.id,
                                     text=answers[3],
                                     reply_markup=menu())

                else:
                    bot.send_message(chat_id=message.chat.id,
                                     text='Эта ссылка не поддерживается(\nПопробуй ещё раз',
                                     reply_markup=del_markups)


if __name__ == '__main__':
    print('bot is now polling')

    bot.polling(non_stop=True)
