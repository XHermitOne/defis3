#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль прикладной системы. Оценки состояния по набору индикаторов (карте).
Используем образы некоторых известных состояний в качестве классификаторов, по которым
определяем комплексную оцнку состояния.
"""

from analitic.usercomponents import icarrowindicator
from ic.bitmap import ic_bmp

# Версия
__version__ = (0, 1, 1, 1)


# --- Функции
def differece(m1, m2):
    """
    Вычисляет степень различия между матрицами m1, m2.
    """
    D = 0
    for i, r in enumerate(m1):
        for j, v1 in enumerate(r):
            if len(m2) > i and len(m2) > j:
                v2 = m2[i][j]
            else:
                v2 = 0
            D += (v2-v1) ^ 2
    return D


def convertValToState():
    """
    """
    pass


# --- Классы
class IndGroup:
    """
    Класс группы индикаторов.
    """
    def __init__(self, valLst):
        """
        Конструктор.

        @type valLst: C{list}
        @param valLst: Список значений индикаторов.
        """
        self.grp = valLst

    def difference(self, ob):
        """
        Вычисдяется степень различия между текщей группой индикаторов и группой
        индикаторов задающей определенное состояние.

        @type ob: C{IndGroup}
        @param ob: Группа индикаторов, с которой производится сравнение.
        """
        D = 0
        for i, x in self.grp:
            if len(ob) < i:
                D += (x - ob[i]) ^ 2
            else:
                D += x ^ 2

        return D


class ColorIndGroup(IndGroup):
    """
    Группа цветовых показателей. У каждого показателя только четыре состояния:
        1. Не определено (серый)
        2. Плохо (красный)
        3. Переходное состояние (желтый)
        4. Хорошо (зеленый)
    """
    UNDEFINE_STATE = 0
    RED_STATE = 1
    YELLOW_STATE = 2
    GREEN_STATE = 3

    def __init__(self, valLst, descr=None):
        """
        Конструктор.

        @type valLst: C{list}
        @param valLst: Список значений индикаторов.
        @type descr: C{list}
        @param descr: Описание цветовых зон.
        """
        #   Описание цветовых зон
        if descr is None:
            self._descr = [('45%', 'RED'), ('50%', (255, 200, 0)), ('100%', 'GREEN')]
        else:
            self._descr = descr

        #   Текущее состояние обобщенного индикаторв
        self._state = ColorIndGroup.UNDEFINE_STATE

        IndGroup.__init__(self, valLst)


def getState_RZMonitor(metaObj):
    """
    Возвращает оценку состояние группы мониторов по реализации и заявкам.

    @type metaObj: C{icMetaItem}
    @param metaObj: Указатель на классификатор мониторов.
    """


def getStateImage(filename, state):
    """
    Возвращает нужную картинку в зависимости от состояния группы индикаторов.
    """
    st1, st2 = state
    pref1, pref2 = '',''

    d = {ColorIndGroup.UNDEFINE_STATE:'',
         ColorIndGroup.RED_STATE:'R',
         ColorIndGroup.YELLOW_STATE:'Y',
         ColorIndGroup.GREEN_STATE:'G'}

    try:
        pref1, pref2 = d[st1], d[st2]
    except:
        print('Invalid state identificator state=:', state)

    if pref1 and pref2:
        # print 'pic name=', filename.replace('.gif',pref1+pref2+'.gif')
        return ic_bmp.getUserBitmap(filename.replace('.gif', pref1 + pref2 + '.gif'), 'plan')
    else:
        return ic_bmp.getUserBitmap(filename, 'plan')
#    if state == ColorIndGroup.RED_STATE:
#        return lib.GetUserBitmap(filename.replace('.gif','Red.gif'), 'plan')
#    elif state == ColorIndGroup.YELLOW_STATE:
#        return lib.GetUserBitmap(filename.replace('.gif','Yell.gif'), 'plan')
#    elif state == ColorIndGroup.GREEN_STATE:
#        return lib.GetUserBitmap(filename.replace('.gif','Green.gif'), 'plan')
#    else:
#        return lib.GetUserBitmap(filename, 'plan')


def test():
    """
    """
    d = ColorIndGroup([])


if __name__ == '__main__':
    test()
