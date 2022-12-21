#!/usr/bin/env python3
####
from os import remove
import subprocess
import sys
from time import sleep
import telebot;
import yt_dlp;
import datetime
import time

def help():
    print('Create bot in https://t.me/BotFather and put token to script or with -t argument')
    print('-t <token_string> - puts telegram bot token to script')
token = ''

argIdx = 1
while(argIdx < len(sys.argv)):
    if sys.argv[argIdx] == '-t':
        if (argIdx + 1 >= len(sys.argv)):
            print('token expected after -t')
            quit()
        else:
            token = sys.argv[argIdx + 1]
            argIdx += 1
    elif sys.argv[argIdx] == '-h':
        help()
        quit()
    else:
        print('{} - unknown arg'.format(sys.argv[argIdx]))
        help()
        quit()
    argIdx += 1

bot = telebot.TeleBot(token)
counter = 0

with open('log.txt', 'a') as f:
    f.write("launched {}\n".format(datetime.datetime.now()))

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if (message.text == '/start'):
        bot.send_message(message.from_user.id, 'Отправь ссылку на тикток или ютуб')
    elif (message.text == '/help'):
        bot.send_message(message.from_user.id, 'Отправь ссылку на тикток или ютуб')
    else:
        global counter
        counter += 1
        current_counter = counter

        try:
            print('{} try load: {}'.format(current_counter, message.text))
            bot.send_message(message.from_user.id, 'Работаем')

            try:
                yt_dlp.YoutubeDL({
                    'no_warnings': True,
                    'quiet': True,
                    'outtmpl': 'video{}.mp4'.format(current_counter)
                }).download(message.text)
            except:
                with open('log.txt', 'a') as f:
                    f.write("{} failed {} request {}\n".format(current_counter, message.from_user.id, message.text))
                bot.send_message(message.from_user.id, 'Нерабочая ссылка')
            print('{} loaded::: {}'.format(current_counter, message.text))
            
            bot.send_video(message.from_user.id, video=open('video{}.mp4'.format(current_counter), 'rb'))
            print('{} sended::: {}'.format(current_counter, message.text))
            
            remove('video{}.mp4'.format(current_counter))
            with open('log.txt', 'a') as f:
                f.write("{} success {} request {}\n".format(current_counter, message.from_user.id, message.text))
        except:
            with open('log.txt', 'a') as f:
                f.write("{} bot failed {} request {}\n".format(current_counter, message.from_user.id, message.text))
            print('telegram bot died')
        print('{} done::::: {}'.format(current_counter, message.text))
while(True):
    try:
        bot.polling(none_stop=True, interval=0)
        print('telegram bot restart')
        with open('log.txt', 'a') as f:
            f.write("{} bot restart\n".format(counter))
    except:
        print('telegram bot died in loop')
        with open('log.txt', 'a') as f:
            f.write("{} bot died. Restarting\n".format(counter))
        sleep(15)
