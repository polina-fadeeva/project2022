import telebot
from telebot import types
import conf
from gettext import find
from urllib import response
import requests
from bs4 import BeautifulSoup

# import sbornik
# from sbornik import lermontov
bot = telebot.TeleBot(conf.TOKEN)
# bot.remove_webhook()

 
# def get_line(word):
#     url = f'https://istihi.ru/lermontov'
#     r = requests.get(url).text
#     soup = BeautifulSoup(r, 'lxml')
#     block = soup.find('ol', {'class': "author-poem-list"})
#     all_stihi = block.find_all('li')
#     flag = False
#     for stih in all_stihi:
#         href = stih.find('a').get('href')
#         stih_link = 'https://istihi.ru' + href
#         r = requests.get(stih_link).text
#         soup = BeautifulSoup(r, 'lxml')
#         block = soup.find('div', {'class': "poem-text"})
#         for line in block.text.split('\n'):
#             if len(line.lower().split()) != 0:
#                 if word == line.lower().split()[-1]:
#                     return line


d = dict()
d['к'] =  'г'
d['г'] =  'к'
d['п'] =  'б'
d['б'] =  'п'
d['д'] =  'т'
d['т'] =  'д'
d['в'] =  'ф'
d['ф'] =  'в'
d['з'] =  'с'
d['с'] =  'з'
d['ш'] =  'ж'
d['ж'] =  'ш'
d['а'] =  'о'
d['о'] =  'а'
d['и'] =  'е'
d['е'] =  'и'
 
def is_same_letters(letter1, letter2):
    if letter1 == letter2:
        return True
    if letter1 in d and d[letter1] == letter2:
        return True
    return False
 
def is_same_words(word1, word2):
    if len(word1) == 0 or len(word1) == 0:
        return False
    return is_same_letters(word1[-1],word2[-1])
 
def get_line(word):
    url = f'https://istihi.ru/lermontov'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    block = soup.find('ol', {'class': "author-poem-list"})
    all_stihi = block.find_all('li')
    flag = False
    for stih in all_stihi:
        href = stih.find('a').get('href')
        stih_link = 'https://istihi.ru' + href
        r = requests.get(stih_link).text
        soup = BeautifulSoup(r, 'lxml')
        block = soup.find('div', {'class': "poem-text"})
        lines = block.text.split('\n')
        for i,line in enumerate(lines):
            if len(line.lower().split()) != 0:
                new_word = line.lower().strip().split()[-1].strip(',.!?:;"\')(')
                if word == new_word:
                    lenght = 1
                    while True:
                        
                        if i - lenght < 0 and i+ lenght >= len(lines):
                            break
                        if i - lenght >= 0:
                            same_word = lines[i-lenght].lower().strip().split()[-1].strip(',.!?:;"\')(')
                            if is_same_words(same_word,word):
                                return lines[i-lenght]
                        if i+ lenght < len(lines):
                            same_word = lines[i+lenght].lower().strip().split()[-1].strip(',.!?:;"\')(')
                            # print(is_same_letters(same_word[-1]))
                            # break
                            if is_same_words(same_word,word):
                                return lines[i+lenght]
                        lenght += 1

@bot.message_handler(commands=["start", 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я - бот-рифмоплёт. Отправь мне любое слово, а я постараюсь ответить в рифму строчкой одного из стихотворений М. Ю. Лермонтова!")


@bot.message_handler(content_types=["text"])
def text(message):
    clippy = open('skrepka.gif', 'rb')
    bot.send_video(message.chat.id, clippy)
    clippy.close()
    bot.send_message(message.chat.id, 'Ищу рифму...')
    soob = message.text
    
    splitter = str.split(soob)
    slovo_user = splitter[-1]
    line = get_line(slovo_user)
    # if slovo_user in lermontov:
    #     lrmntv_split = tk.tokenize(lermontov)
    #     for smth in lrmntv_split:
    #         if slovo_user in smth:
    #             razdel = smth.split()
    #             if slovo_user == razdel[-1]:
    #                 number = lrmntv_split.index(smth) + 2
    #             if number < len(lrmntv_split):
    #                 print (lrmntv_split[number])
    #             else:
    #                 number2 = lrmntv_split.index(smth) - 2
    #                 print(lrmntv_split[number2])
    bot.send_message(message.chat.id, line)
    
if __name__ == '__main__':
    bot.polling(none_stop=True)


    
