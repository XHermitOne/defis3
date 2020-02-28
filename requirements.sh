# !/bin/sh

# Пакеты необходимые для работы проектов на Python:
# Тестирование проводилось на Ubuntu 18.04.LTS

sudo apt install --assume-yes python3-pip

# Анализаторы кода Python
sudo apt install --assume-yes pylint3

sudo apt install --assume-yes python3-pep8

# Модули ОС
sudo apt install --assume-yes smbfs-utils

sudo apt install --assume-yes cifs-utils

sudo apt install --assume-yes smbclient

sudo apt install --assume-yes indicator-applet-complete

sudo apt install --assume-yes ttf-mscorefonts-installer

sudo apt install --assume-yes python3-apt

# Работа с консолью
sudo apt install --assume-yes python3-dialog

sudo apt install --assume-yes python3-urwid

sudo apt install --assume-yes curl

sudo apt install --assume-yes libsdl1.2debian

# wxPython

# Необходимо для сборки wxPython
sudo apt install --assume-yes libsdl2-2.0-0
sudo apt install --assume-yes build-essential libgtk-3-dev
# Поддержка web в wxPython
# sudo apt install --assume-yes libwebkitgtk-3.0-0
sudo apt install --assume-yes libwebkit2gtk-4.0-dev

# Установка для Ubuntu 16.04
pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython

# Обновление:
# pip3 install wxPython --upgrade
# Удаление:
# pip3 uninstall wxPython

# Установка для Ubuntu 18.04
# pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython

# Альтернативный способ установки
# pip3 download wxPython
# pip3 wheel -v wxPython-4.0.1.tar.gz  2>&1 | tee build.log
# pip3 install wxPython-4.0.1-cp35-cp35m-linux_x86_64.whl

pip3 install objectlistview

sudo apt install --assume-yes python3-six

sudo apt install --assume-yes python3-matplotlib

# Нет в репозитариях
# sudo apt install --assume-yes python3-wxmpl

# БД
sudo apt install --assume-yes python3-psycopg2
sudo apt install --assume-yes python3-mysqldb
sudo apt install --assume-yes python3-sqlalchemy
sudo apt install --assume-yes unixodbc unixodbc-dev freetds-bin freetds-dev tdsodbc python3-pyodbc

# pip3 install dbfpy
# Работу с DBF везде необходимо делать через JDBC
pip3 install JayDeBeApi
# pip3 install JayDeBeApi3

pip3 install dbfread

# Office
sudo apt install --assume-yes unoconv

sudo apt install --assume-yes python3-sane

sudo apt install --assume-yes python3-reportlab

sudo apt install --assume-yes python3-pypdf2

sudo apt install --assume-yes python3-odf python-odf-doc

sudo apt install --assume-yes libreoffice-java-common

sudo apt --fix-broken install --assume-yes

# Установка ic.pth
sudo cp ./ic.pth /usr/lib/python3/dist-packages
echo +++++++++++++++++++++++++++++++
echo +   Проект DEFIS3 установлен  +
echo +++++++++++++++++++++++++++++++
