# !/bin/sh

sudo apt install --assume-yes python3-pip

pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython
sudo apt install --assume-yes python3-psycopg2
sudo apt install --assume-yes python3-sqlalchemy
sudo apt install --assume-yes python3-matplotlib
sudo apt install --assume-yes python3-odf python-odf-doc

sudo apt install --assume-yes smbclient
pip3 install PySmbClient

sudo cp /mnt/defis/defis3/ic.pth /usr/lib/python3/dist-packages

sudo apt --fix-broken install --assume-yes
