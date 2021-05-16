! /bin/sh
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install python3.9
sudo apt -y install python3.9-distutils
python3.9 -m pip install --user virtualenv

sudo apt-get install apache2  php libapache2-mod-php php-mcrypt
sudo systemctl restart apache2

sudo cp -r WebSecAsst /var/www/html/
sudo mkdir /var/www/html/WebSecAsst/venv
sudo chmod 777 /var/www/html/WebSecAsst
sudo chmod 777 /var/www/html/WebSecAsst/*
sudo python3.9 -m venv /var/www/html/WebSecAsst/venv/websecasst
sudo chmod 777 /var/www/html/WebSecAsst/venv/*
sudo /var/www/html/WebSecAsst/venv/websecasst/bin/python3.9 get-pip.py
sudo /var/www/html/WebSecAsst/venv/websecasst/bin/python3.9 -m pip install dist/WebSecAsst-1.0.1-py3-none-any.whl