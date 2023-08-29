# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Copy the current directory contents into the container
COPY bot/bot_script.py /app/bot_script.py
COPY bot/requirements.txt /app/requirements.txt

# Set the working directory in the container
WORKDIR /app

RUN apk add update && \
    apk add install -y ffmpeg && \
    rm -rf /var/cache/apk/* && \
    pip install -r /app/requirements.txt && \
    chmod +x /app/bot_script.py

# Run the bot_script.py when the container launches
CMD ["python3", "/app/bot_script.py"]
