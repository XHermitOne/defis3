# !/bin/sh

# Пакеты необходимые для работы проектов на Python:
# Тестирование проводилось на Ubuntu 16.04.LTS

# Анализаторы кода Python
apt show pylint | grep Package
apt show pylint | grep Version
sudo apt install pylint

apt show python-pep8 | grep Package
apt show python-pep8 | grep Version
sudo apt install python-pep8

# Модули ОС
apt show smbfs-utils | grep Package
apt show smbfs-utils | grep Version
sudo apt install smbfs-utils

apt show cifs-utils | grep Package
apt show cifs-utils | grep Version
sudo apt install cifs-utils

apt show smbclient | grep Package
apt show smbclient | grep Version
sudo apt install smbclient

apt show indicator-applet-complete | grep Package
apt show indicator-applet-complete | grep Version
sudo apt install indicator-applet-complete

apt show ttf-mscorefonts-installer | grep Package
apt show ttf-mscorefonts-installer | grep Version
sudo apt install ttf-mscorefonts-installer

apt show python-apt | grep Package
apt show python-apt | grep Version
sudo apt install python-apt

# Работа с консолью
apt show python-dialog | grep Package
apt show python-dialog | grep Version
sudo apt install python-dialog

apt show python-urwid | grep Package
apt show python-urwid | grep Version
sudo apt install python-urwid

apt show curl | grep Package
apt show curl | grep Version
sudo apt install curl

# wxPython
apt show python-wxgtk3.0 | grep Package
apt show python-wxgtk3.0 | grep Version
sudo apt install python-wxgtk3.0

apt show python-six | grep Package
apt show python-six | grep Version
sudo apt install python-six

apt show python-matplotlib | grep Package
apt show python-matplotlib | grep Version
sudo apt install python-matplotlib

apt show python-wxmpl | grep Package
apt show python-wxmpl | grep Version
sudo apt install python-wxmpl

# БД
apt show python-psycopg2 | grep Package
apt show python-psycopg2 | grep Version
sudo apt install python-psycopg2

apt show python-sqlalchemy | grep Package
apt show python-sqlalchemy | grep Version
sudo apt install python-sqlalchemy

apt show python-pyodbc | grep Package
apt show python-pyodbc | grep Version
sudo apt install unixodbc unixodbc-dev freetds-bin freetds-dev tdsodbc python-pyodbc

# Office
apt show unococnv | grep Package
apt show unococnv | grep Version
sudo apt install unoconv

apt show python-sane | grep Package
apt show python-sane | grep Version
sudo apt install python-sane

apt show python-reportlab | grep Package
apt show python-reportlab | grep Version
sudo apt install python-reportlab

apt show python-pypdf2 | grep Package
apt show python-pypdf2 | grep Version
sudo apt install python-pypdf2

apt show python-odf | grep Package
apt show python-odf | grep Version
sudo apt install python-odf python-odf-doc

apt show libreoffice-java-common | grep Package
apt show libreoffice-java-common | grep Version
sudo apt install libreoffice-java-common

# В конце отобразим список установленных пакетов

echo
echo ============================
echo Установлены следующие пакеты
echo ============================

echo
echo Анализаторы кода Python
echo
apt show pylint | grep Package
apt show pylint | grep Version

apt show python-pep8 | grep Package
apt show python-pep8 | grep Version

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

apt show python-apt | grep Package
apt show python-apt | grep Version


echo
echo Работа с консолью
echo
apt show python-dialog | grep Package
apt show python-dialog | grep Version

apt show python-urwid | grep Package
apt show python-urwid | grep Version

apt show curl | grep Package
apt show curl | grep Version

echo
echo wxPython
echo
apt show python-wxgtk3.0 | grep Package
apt show python-wxgtk3.0 | grep Version

apt show python-six | grep Package
apt show python-six | grep Version

apt show python-matplotlib | grep Package
apt show python-matplotlib | grep Version

echo
echo БД
echo
apt show python-psycopg2 | grep Package
apt show python-psycopg2 | grep Version

apt show python-sqlalchemy | grep Package
apt show python-sqlalchemy | grep Version

apt show python-pyodbc | grep Package
apt show python-pyodbc | grep Version

echo
echo Office
echo
apt show unococnv | grep Package
apt show unococnv | grep Version

apt show python-sane | grep Package
apt show python-sane | grep Version

apt show python-reportlab | grep Package
apt show python-reportlab | grep Version

apt show python-pypdf2 | grep Package
apt show python-pypdf2 | grep Version

apt show python-odf | grep Package
apt show python-odf | grep Version

apt show libreoffice-java-common | grep Package
apt show libreoffice-java-common | grep Version

# Установка ic.pth
sudo cp ./ic.pth /usr/lib/python2.7/dist-packages
echo +++++++++++++++++++++++++++++++
echo |   Проект DEFIS установлен   |
echo +++++++++++++++++++++++++++++++
