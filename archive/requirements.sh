# !/bin/sh

sudo apt install --assume-yes python3-pip

sudo apt install --assume-yes nfs-kernel-server nfs-common

# pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython==4.0.4
pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython==4.0.7.post2 Pillow==7.0.0 numpy==1.16.6
sudo apt install --assume-yes python3-psycopg2
sudo apt install --assume-yes python3-sqlalchemy
sudo apt install --assume-yes python3-six
# sudo apt install --assume-yes tesseract-ocr tesseract-ocr-rus
sudo apt install --assume-yes unoconv
sudo apt install --assume-yes python3-sane
sudo apt install --assume-yes python3-reportlab
sudo apt install --assume-yes git
sudo apt install --assume-yes python3-mysqldb

sudo apt install --assume-yes smbclient
pip3 install PySmbClient

# pip3 install dbfpy
git clone https://github.com/phargogh/dbfpy3
sudo python3 ./dbfpy3/setup.py install

pip3 install dbfread

sudo apt install --assume-yes pdftk

sudo apt --fix-broken install --assume-yes
