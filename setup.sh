sudo apt update
sudo apt-get -y install python3-pip
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
PATH="/users/$USER/.local/bin:$PATH"
sudo git clone https://github.com/CMahk/yolov5.git
cd ./yolov5
pip3 install -r requirements.txt
