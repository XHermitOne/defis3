#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс менеджера управления утилитой построения графиков gnuplot.

Примеры комманд использования gnuplot:

gnuplot -e "set xdata time;set timefmt '%H:%M:%S';set format x '%H:%M:%S';set xrange['00:00:00':'00:00:15'];set terminal png;set style line 1 lt 1 lw 1 pt 3 linecolor rgb 'red';set grid;set nokey;set xtics rotate;set term png size 1024,600;set output 'trend.png';plot './trend.txt' using 1:2 with lines linestyle 1"
eog ./trend.png
"""

# Версия
__version__ = (0, 1, 1, 1)


class icGnuplotManager(object):
    """
    Класс менеджера управления утилитой построения графиков gnuplot.
    """
