#!/bin/bash

# Update package lists
sudo apt update

# Install Docker and answer 'Y' when prompted
 sudo apt install -y docker.io

#Build Yolo5 app image

sudo docker build -t -t my_app:0.0.1 .

# Run the Docker container with the 'always' restart policy
sudo docker run --restart always my_app:0.0.1