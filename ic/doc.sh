# Установка Sphinx:
# sudo apt install python3-sphinx

# Если не будет производится импорт модулей необходимо добавить в conf.py
# пути для поиска. 
# Например:
# import os
# import sys
# sys.path.append(os.path.abspath('../..'))

# Генерация документации:
# ВНИМАНИЕ! Нельзя использовать ключ --force при генерации документации
# т.к. перезаписывается файл conf.py
sphinx-apidoc --separate --full --output-dir ./doc .
make -C ./doc/ html
