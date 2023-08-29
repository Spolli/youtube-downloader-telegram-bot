# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Copy the current directory contents into the container
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Make bot_script.py executable
RUN chmod +x bot_script.py

# Run the bot_script.py when the container launches
CMD ["python3", "bot_script.py"]
