#!/bin/bash
apt update -y
apt install -y python3-pip git

cd /home/ubuntu
git clone https://github.com/goulartandrey/library.git
cd library

pip3 install -r requirements.txt


nohup uvicorn main:app --host 0.0.0.0 --port 80 &
