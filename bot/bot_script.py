import os
import telebot
from pytube import YouTube
from moviepy.editor import VideoFileClip

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ALLOWED_CHAT_ID = os.environ.get('ALLOWED_CHAT_ID')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(func=lambda message: message.chat.id == ALLOWED_CHAT_ID)
def handle_message(message):
    if message.text.startswith("https://www.youtube.com"):
        try:
            youtube_url = message.text
            video = YouTube(youtube_url)
            
            # Get the highest resolution stream available
            stream = video.streams.get_highest_resolution()
            
            # Download the video
            bot.reply_to(message, "Downloading video...")
            video_path = stream.download()
            
            # Convert video to MP3
            bot.reply_to(message, "Converting to MP3...")
            video_clip = VideoFileClip(video_path)
            mp3_path = video_path.replace(".mp4", ".mp3")
            video_clip.audio.write_audiofile(mp3_path)
            
            # Send the MP3 file
            bot.reply_to(message, "Sending MP3...")
            with open(mp3_path, 'rb') as mp3_file:
                bot.send_audio(ALLOWED_CHAT_ID, mp3_file)
            
            # Clean up downloaded files
            os.remove(video_path)
            os.remove(mp3_path)
            
            bot.reply_to(message, "Process complete.")
            
        except Exception as e:
            bot.reply_to(message, f"An error occurred: {e}")
    else:
        bot.reply_to(message, "Please provide a valid YouTube link.")

bot.polling()