# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir pyTelegramBotAPI pytube

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Make bot_script.py executable
RUN chmod +x bot/bot_script.py

# Set environment variables
ENV TELEGRAM_BOT_TOKEN=5449367848:AAH3fCtqxv1Ryhp1zXI8C1jJEbMyvpff0rw
ENV ALLOWED_CHAT_ID=958468633

# Run the bot_script.py when the container launches
CMD ["python3", "bot/bot_script.py"]
