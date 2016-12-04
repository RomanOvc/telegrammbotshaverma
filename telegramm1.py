import os
import re
import logging
import telebot
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot('328238493:AAEZPnI4hdrSXdmv_ICdCfvModJCRIHIp6E')


@bot.message_handler(commands=['start'])
def SendInfo(message):
    bot.send_message(message.chat.id, 'Привет!,я ШаВеРнЫй бОгТ')


@bot.message_handler(commands=['text'])
def SendInfo(message):
    images = SearchGoogleImages(message.text[6:], message.chat.id)
    for image in images:
         bot.send_photo(message.chat.id, open(image, 'rb'))


def SearchGoogleImages(query, id):
    path = os.path.abspath(os.curdir)
    path = os.path.join(path, str(id))
    print('path=' + path)

    if not os.path.exists(path):
        os.makedirs(path)

    url = 'https://www.google.ru/search?q=' + query + '&newwindow=1&tbm=isch'
    request = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, Chrome/43.0.2357.134 Safari/537.36'})
    print(query)
    print(url)
    soup = bs(request.content, "html.parser")
    images = soup.find_all('div', attrs={'class': re.compile("rg_meta")})

    imagesPaths = []

    for count, image in enumerate(images[:5]):

        print(str(image) + '\n')
        atr = str(image)[str(image).find('ou":"') + 5:]
        atr = atr[:atr.find('"')]
        img = requests.get(atr)
        image = Image.open(BytesIO(img.content))
        imgpath = os.path.join(path, str(count) + '.jpg')
        image.save(imgpath)
        print(imgpath)
        imagesPaths.append(imgpath)

    return imagesPaths

if __name__ == '__main__':
    logging.basicConfig(filename='botlog.log',
    format='%(filename)s[LINE:%(lineno)d]# %(levelname) -8s [%(asctime)s] %(message)s',
    level=logging.DEBUG)
    logging.info('Bot started!')

    try:
        bot.polling(none_stop=True)
    except Exception:
        logging.critical('ERROR...')
    finally:
          bot.polling(none_stop=True)
