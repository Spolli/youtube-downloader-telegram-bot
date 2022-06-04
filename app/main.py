#!/usr/bin/env python3

from __future__ import unicode_literals
import youtube_dl
import telebot
import os

TOKEN = os.environ("TOKEN") if "TOKEN" in os.environ else ""
USERNAME = os.environ("USERNAME") if "USERNAME" in os.environ else ""
PASSWORD = os.environ("PASSWORD") if "PASSWORD" in os.environ else ""

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(regexp="^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$")
def handle_message(message):
    ydl_opts = {
        'username': USERNAME,
        'password': PASSWORD,
        'format': 'bestaudio/best',
        'outtmpl': './download/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'prefer_ffmpeg': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([message.text])
    bot.reply_to(message, "Howdy, how are you doing?")

if __name__ == '__main__':
    bot.infinity_polling()


