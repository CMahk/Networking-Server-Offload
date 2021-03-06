sudo apt update
sudo apt-get -y install python3-pip
sudo apt-get -y install ffmpeg libsm6 libxext6
PATH="/users/$USER/.local/bin:$PATH"
sudo git clone https://github.com/CMahk/yolov5.git
cd ./yolov5
pip3 install -r requirements.txt
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
pip3 install psutil
yes | sudo ufw enable
sudo ufw allow 25565
