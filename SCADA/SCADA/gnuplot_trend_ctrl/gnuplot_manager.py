#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс менеджера управления утилитой построения графиков gnuplot.

Примеры комманд использования gnuplot:

gnuplot -e "
set xdata time;
set timefmt '%H:%M:%S';
set format x '%H:%M:%S';
set xrange['00:00:00':'00:00:15'];
set terminal png;
set style line 1 lt 1 lw 1 pt 3 linecolor rgb 'red';
set grid;
set nokey;
set xtics rotate;
set term png size 1024,600;
set output 'trend.png';
plot './trend.txt' using 1:2 with lines linestyle 1
"

eog ./trend.png
"""

import os
from ic.log import log
from ic.utils import txtfunc

# Версия
__version__ = (0, 1, 1, 1)

# Разделитель комманд gnuplot
COMMAND_DELIMETER = ';'

GNUPLOT_COMMAND_FMT = 'gnuplot -e \"%s\"'


class icGnuplotManager(object):
    """
    Класс менеджера управления утилитой построения графиков gnuplot.
    """
    def __init__(self):
        """
        Конструктор.
        """
        # Список комманд для последующей
        # генерации коммандной строки запуска gnuplot
        self.commands = list()

        self.__x_format = None

    def _findCommand(self, command_word):
        """
        Поиск комманды в списке комманд по ключевому слову.
        @param command_word: Ключевое слово.
        @return: Индекс в списке комманд или -1 если такая команда не найдена.
        """
        for i, command in enumerate(self.commands):
            if command_word in command:
                return i
        return -1

    def _appendCommand(self, command, command_word=None):
        """
        Произвести добавление комманды в список комманд.
        Если в списке найдена комманда по ключевому слову, то она заменяется.
        Если не найдена, то просто команда добавляется в список.
        @param command: Комманда.
        @param command_word: Ключевое слово.
            Если None, то просто происходит добавление команды в список.
        @return: True/False.
        """
        if command_word is None:
            # Просто добавить команду в список
            self.commands.append(command)
        else:
            # Сначала производим поис уже существующей команды
            # в списке по ключевому слову
            find_idx = self._findCommand(command_word)
            if find_idx >= 0:
                # Если есть таккая команда, то заменяем ее
                self.commands[find_idx] = command
            else:
                # Если команда не найдена, то просто заменяем ее
                self.commands.append(command)
        return True

    def _enableCommand(self, command, enable=True):
        """
        Включить/Исключить комманду из списка комманд.
        @param command: Комманда gnuplot.
        @param enable: True - включить комманду/False - исключить комманду.
        @return: True/False.
        """
        if enable:
            if command not in self.commands:
                self.commands.append(command)
        else:
            if command in self.commands:
                del self.commands[self.commands.index(command)]
        return True

    def enableXTime(self, enable=True):
        """
        Вкл./Выкл. оси X как временной.
        @param enable: True - включить/False - выключить.
        @return: True/False.
        """
        cmd = 'set xdata time'
        return self._enableCommand(cmd, enable)

    def setTimeFormat(self, dt_format=None):
        """
        Установить формат даты-времени.
        @param dt_format: Формат даты-времени.
            Если None, то установка формата исключается из списка комманд.
        @return: True/False.
        """
        cmd_sign = 'set timefmt'
        cmd = 'set timefmt \'%s\'' % dt_format
        return self._appendCommand(cmd, cmd_sign)

    def setXFormat(self, x_format=None):
        """
        Установить формат оси X.
        @param x_format: Формат оси X.
            Если None, то установка формата исключается из списка комманд.
        @return: True/False.
        """
        cmd_sign = 'set format x'
        cmd = 'set format x \'%s\'' % x_format
        # Запоминаем формат оси X для правильного вывода данных
        # в файл данных графиков
        self.__x_format = x_format
        return self._appendCommand(cmd, cmd_sign)

    def setXRange(self, x_start, x_stop):
        """
        Установить диапазон значений оси X.
        @param x_start: Начальное значение диапазона.
        @param x_stop: Конечное значение диапазона.
        @return: True/False.
        """
        cmd_sign = 'set xrange'
        cmd = 'set xrange[\'%s\':\'%s\']' % (x_start, x_stop)
        return self._appendCommand(cmd, cmd_sign)

    def enableXTextVertical(self, enable=True):
        """
        Вкл./Выкл. вывода текста оси X вертикально.
        @param enable: True - включить/False - выключить.
        @return: True/False.
        """
        cmd = 'set xtics rotate'
        return self._enableCommand(cmd, enable)

    def enableOutputPNG(self, enable=True):
        """
        Вкл./Выкл. вывода графика в формате PNG.
        @param enable: True - включить/False - выключить.
        @return: True/False.
        """
        cmd = 'set terminal png'
        return self._enableCommand(cmd, enable)

    def setOutputSize(self, width, height):
        """
        Установить размер результирующей картинки.
        @param width: Ширина.
        @param height: Высота.
        @return: True/False.
        """
        cmd_sign = 'set term png size'
        cmd = 'set term png size %d, %d' % (int(width), int(height))
        return self._appendCommand(cmd, cmd_sign)

    def setOutputFilename(self, out_filename):
        """
        Установить имя результирующего файла.
        @param out_filename: Полное имя результирующего файла.
        @return: True/False.
        """
        cmd_sign = 'set output'
        cmd = 'set output \'%s\'' % out_filename
        return self._appendCommand(cmd, cmd_sign)

    def enableGrid(self, enable=True):
        """
        Вкл./Выкл. сетки.
        @param enable: True - включить сетку/False - выключить.
        @return: True/False.
        """
        cmd = 'set grid'
        return self._enableCommand(cmd, enable)

    def enableLegend(self, enable=True):
        """
        Вкл./Выкл. легенды.
        @param enable: True - включить легенду/False - выключить.
        @return: True/False.
        """
        cmd = 'set nokey'
        return self._enableCommand(cmd, enable)

    def setLineStyle(self, n_line=1, line_type=1, line_width=1, point_type=3, line_color='red'):
        """
        Установить стиль линии.
        @param n_line: Номер линии.
        @param line_type: Тип линии.
        @param line_width: Толщина линии.
        @param point_type: Тип точки.
        @param line_color: Цвет линии
        @return: True/False.
        """
        cmd_sign = 'set style line %d' % int(n_line)
        cmd = 'set style line %d linetype %d linewidth %d pointtype %d linecolor rgb \'%s\'' % (int(n_line),
                                                                                                int(line_type),
                                                                                                int(line_width),
                                                                                                int(point_type),
                                                                                                line_color)
        return self._appendCommand(cmd, cmd_sign)

    def setPlot(self, graph_filename, count=1):
        """
        Установить отрисовку графиков.
        @param graph_filename: Полное имя файла данных графиков.
        @param count: Количество графиков.
        @return: True/False.
        """
        cmd_sign = 'plot '
        cmd = 'plot \'%s\' using 1:%d with lines linestyle 1' % (graph_filename, int(count))

        # Команда отрисовки графиков может быть только последней коммандой
        if not self.commands:
            self.commands.append(cmd)
        else:
            last_cmd = self.commands[-1]
            if last_cmd.startswith(cmd_sign):
                self.commands[-1] = cmd
            else:
                self.commands.append(cmd)
        return True

    def saveGraphData(self, graph_filename, graph_data=(), fields=()):
        """
        Записать данные графиков в файл данных.
        @param graph_filename: Полное имя файла данных графиков.
        @param graph_data: Список словарей данных графиков.
            [
                {
                    'x': Значение координаты X,
                    'Имя графика 1': Значение координаты Y графика 1,
                    'Имя графика 2': Значение координаты Y графика 2,
                    ...
                    'Имя графика N': Значение координаты Y графика N,
                }, ...
            ]
        @param fields: Порядок следования графиков в файле данных.
            ['Имя графика 1', 'Имя графика 2', ... 'Имя графика N']
        @return: True/False.
        """
        txt = ''
        for record in graph_data:
            x = record.get('x', 0)
            x_str = str(x) if self.__x_format is None else x.strftime(self.__x_format)
            record_list = [x_str] + [str(record.get(field, 0)) for field in fields]
            record_txt = ' '.join(record_list)
            txt += record_txt + '\n'
        return txtfunc.save_file_text(graph_filename, txt)

    def getRunCommand(self):
        """
        Получить результирующую комманду для запуска генерации.
        @return: Результирующая комманда для генерации файла графика.
        """
        commands = COMMAND_DELIMETER.join(self.commands)
        return GNUPLOT_COMMAND_FMT % commands

    def runCommands(self):
        """
        Запуск генерации.
        @return: True/False.
        """
        cmd = self.getRunCommand()
        log.info(u'Выполнение комманды <%s>' % cmd)
        os.system(cmd)
        return True
