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

# Установка для Ubuntu 16.04
# pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython

# Обновление:
# pip3 install wxPython --upgrade
# Удаление:
# pip3 uninstall wxPython

# Установка для Ubuntu 18.04
pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython

# Поддержка web в wxPython
sudo apt install --assume-yes libwebkitgtk-3.0-0

pip3 install objectlistview

sudo apt install --assume-yes python3-six

sudo apt install --assume-yes python3-matplotlib

# Нет в репозитариях
# sudo apt install --assume-yes python3-wxmpl

# БД
sudo apt install --assume-yes python3-psycopg2

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

# В конце отобразим список установленных пакетов

echo
echo ============================
echo Установлены следующие пакеты
echo ============================

echo
echo Анализаторы кода Python
echo
apt show pylint3 | grep Package
apt show pylint3 | grep Version

apt show python3-pep8 | grep Package
apt show python3-pep8 | grep Version

echo
echo Модули ОС
echo
apt show smbfs-utils | grep Package
apt show smbfs-utils | grep Version

apt show cifs-utils | grep Package
apt show cifs-utils | grep Version

apt show smbclient | grep Package
apt show smbclient | grep Version

apt show indicator-applet-complete | grep Package
apt show indicator-applet-complete | grep Version

apt show ttf-mscorefonts-installer | grep Package
apt show ttf-mscorefonts-installer | grep Version

apt show python3-apt | grep Package
apt show python3-apt | grep Version


echo
echo Работа с консолью
echo
apt show python3-dialog | grep Package
apt show python3-dialog | grep Version

apt show python3-urwid | grep Package
apt show python3-urwid | grep Version

apt show curl | grep Package
apt show curl | grep Version

echo
echo wxPython
echo
echo В текущей версии ставиться через pip3
# apt show python-wxgtk3.0 | grep Package
# apt show python-wxgtk3.0 | grep Version

apt show python3-six | grep Package
apt show python3-six | grep Version

apt show python3-matplotlib | grep Package
apt show python3-matplotlib | grep Version

echo
echo БД
echo
apt show python3-psycopg2 | grep Package
apt show python3-psycopg2 | grep Version

apt show python3-sqlalchemy | grep Package
apt show python3-sqlalchemy | grep Version

apt show python3-pyodbc | grep Package
apt show python3-pyodbc | grep Version

echo
echo Office
echo
apt show unococnv | grep Package
apt show unococnv | grep Version

apt show python3-sane | grep Package
apt show python3-sane | grep Version

apt show python3-reportlab | grep Package
apt show python3-reportlab | grep Version

apt show python3-pypdf2 | grep Package
apt show python3-pypdf2 | grep Version

apt show python3-odf | grep Package
apt show python3-odf | grep Version

apt show libreoffice-java-common | grep Package
apt show libreoffice-java-common | grep Version

# Установка ic.pth
sudo cp ./ic.pth /usr/lib/python3/dist-packages
echo +++++++++++++++++++++++++++++++
echo +   Проект DEFIS3 установлен  +
echo +++++++++++++++++++++++++++++++
