import os
import re
import telebot
from pytube import YouTube
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
            if '-' in video.title:
                audiofile = eyed3.load(mp3_path)
                audio_info = video.title.split('-')
                audiofile.tag.artist = remove_enclosed_text(audio_info[0])
                audiofile.tag.title = remove_enclosed_text(audio_info[1])
                audiofile.tag.save()
            
            bot.reply_to(message, "Sending MP3...")
            with open(mp3_path, 'rb') as mp3_file:
                bot.send_audio(ALLOWED_CHAT_ID, mp3_file, caption=f"{video.title}")
            os.remove(audio_path)
            os.remove(mp3_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        bot.reply_to(message, "Please provide a valid YouTube link.")

bot.polling()
