# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

COPY bot/bot_script.py /app/bot_script.py
COPY bot/requirements.txt /app/requirements.txt

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Make bot_script.py executable
RUN chmod +x /app/bot_script.py

# Run the bot_script.py when the container launches
CMD ["python3", "/app/bot_script.py"]
