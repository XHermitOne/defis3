#~/bin/sh

python setup.py bdist_egg
rm ~/dev/ide/Editra-0.7.20/plugins/Defis*.egg
cp ./dist/Defis-0.0.1.2-py2.7.egg ~/dev/ide/Editra-0.7.20/plugins/
