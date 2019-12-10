# Если не будет произвдится импорт модулей необходимо добавить в conf.py
# пути для поиска. Например:
# import os
# import sys
# sys.path.append(os.path.abspath('../..'))

sphinx-apidoc --separate --full --output-dir ./doc .
make -C ./doc/ html
