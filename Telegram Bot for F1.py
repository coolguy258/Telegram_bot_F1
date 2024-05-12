import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

bot = telebot.TeleBot('5574936327:AAGwy6LKiwGx9daYB5EznB7AhvDB0lDKmIw')

@bot.message_handler(commands=['start'])
def srart(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Новости")
    btn2 = types.KeyboardButton("Календарь")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я могу выдать тебе последние новости F1, а также показать расписания заездов.".format(message.from_user), reply_markup=markup)



def get_response(message):
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
    }

    url = f'{"https://www.f1news.ru"}'
    
    # обращаемся к сайту
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text)

    # получаем текст, время и ссылки
    block = soup.find_all('li', class_='b-news-list__item b-news-list__item--with-image')
    for info in block:
        block_title = info.find('a', class_='b-news-list__title').text
        block_time = info.find('a', class_='news_date b-news-list__date').text
        block_url = info.find('a', class_='b-news-list__title', href=True)['href'].strip()

        bot.send_message(message.chat.id, f'{block_title} | {block_time} |\n https://www.f1news.ru{block_url}')



def get_timetable():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
    }

    url = f'{"https://www.f1news.ru/Championship/2022/"}'
    
    # обращаемся к сайту
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text)

    #получаем таблицу 
    timetable = soup.find('table', class_='f1Table wideTable').text
    
    return (timetable)


@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Новости"):
        bot.send_message(message.chat.id, text = get_response(message))
    elif(message.text == "Календарь"):
        bot.send_message(message.chat.id, text = get_timetable())
        
bot.infinity_polling()

