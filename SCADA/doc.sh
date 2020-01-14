# Установка Sphinx:
# sudo apt install python3-sphinx

# Если не будет производится импорт модулей необходимо добавить в conf.py
# пути для поиска. 
# Например:
# import os
# import sys
# sys.path.append(os.path.abspath('..'))

# Генерация документации:
sphinx-apidoc --separate --full --force --output-dir ./doc ./SCADA
make -C ./doc/ html