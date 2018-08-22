# !/bin/sh

sudo apt install --assume-yes nfs-kernel-server nfs-common
pip3 install wxPython
sudo apt install --assume-yes python3-psycopg2
sudo apt install --assume-yes python3-sqlalchemy
sudo apt install --assume-yes python3-six
# sudo apt install --assume-yes tesseract-ocr tesseract-ocr-rus
sudo apt install --assume-yes unoconv
sudo apt install --assume-yes python3-sane
sudo apt install --assume-yes python3-reportlab
sudo apt install --assume-yes git
git clone https://github.com/olemb/dbfread
cd dbfread
sudo python3 setup.py install
