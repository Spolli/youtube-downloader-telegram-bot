#!/bin/bash

# Install system packages
sudo apt-get update
sudo apt-get install -y python3-pip

# Install Python dependencies
cd bot
pip3 install -r requirements.txt

# Copy systemd service file and enable/start the service
sudo cp ../systemd/youtube_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable youtube_bot
sudo systemctl start youtube_bot

echo "Setup completed!"