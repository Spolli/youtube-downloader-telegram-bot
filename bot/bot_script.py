import os
import re
import telebot
from pytube import YouTube
import requests
from io import BytesIO
import cv2
import eyed3

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ALLOWED_CHAT_ID = os.environ.get('ALLOWED_CHAT_ID')

bot = telebot.TeleBot(TOKEN)

youtube_url_pattern = r'(https?://)?(www\.)?youtu(\.be|be\.com)/(watch\?v=|v/|embed/|.*v=)?([^&?/]+)'

def remove_enclosed_text(input_string):
    pattern = r'\([^()]*\)|\[[^\[\]]*\]|\{[^\{\}]*\}'
    result = re.sub(pattern, '', input_string)
    return result

@bot.message_handler(func=lambda message: message.chat.id == int(ALLOWED_CHAT_ID))
def handle_message(message):
    if re.match(youtube_url_pattern, message.text):
        try:
            youtube_url = message.text
            video = YouTube(youtube_url)
            
            audio_stream = video.streams.filter(only_audio=True).first()
            print(video.streams.filter(only_audio=True))
            
            bot.reply_to(message, "Downloading audio...")
            audio_path = audio_stream.download(output_path="audio_temp")
            mp3_path = audio_path.replace(".webm", ".mp3")
            
            # Using ffmpeg to convert audio to MP3
            cmd = f'ffmpeg -i "{audio_path}" -ab 320k -f mp3 "{mp3_path}"'
            os.system(cmd)
            
            # Set artist information and thumbnail image in the MP3 metadata
            audiofile = eyed3.load(mp3_path)
            if '-' in video.title:
                audio_info = video.title.split('-')
                audiofile.tag.artist = remove_enclosed_text(audio_info[0])
                audiofile.tag.title = remove_enclosed_text(audio_info[1])
            try:
                # Fetch the thumbnail URL from video data
                thumbnail_url = video.thumbnail_url
                
                # Download the thumbnail image
                thumbnail_image = requests.get(thumbnail_url)
                image_data = cv2.imencode('.jpg', thumbnail_image)[1].tobytes()
                audiofile.tag.images.set(3, image_data, "image/jpeg", u"Thumbnail") 
            except Exception as e:
                print(f"An error occurred: {e}")
            
            audiofile.tag.save()
            
            bot.reply_to(message, "Sending MP3...")
            with open(mp3_path, 'rb') as mp3_file:
                audio_description = f"{video.title}"
                bot.send_audio(ALLOWED_CHAT_ID, mp3_file, caption=audio_description)
            os.remove(audio_path)
            os.remove(mp3_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        bot.reply_to(message, "Please provide a valid YouTube link.")

bot.polling()
