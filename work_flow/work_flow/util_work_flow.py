#!/usr/bin/env python
#  -*- coding: utf-8 -*-
'''
Вспомогательные функции системы организации бизнес-процессов.
Автор(ы): Колчанов А.В.
'''

# Версия
__version__ = (0, 0, 0, 1)

#--- Подключение библиотек ---
from ic.engine import ic_user
from ic.components import icResourceParser

#--- Функции ---
def browseDocJournal(DocJournalRes_):
    '''
    Открыть журнал документов в режиме управления документами.
    @param DocJournalRes_: Имя ресурса журнала документов.
    '''
    doc_jrnl=icResourceParser.icCreateObject(DocJournalRes_,'mtd')
    print('!!',doc_jrnl)
    doc_jrnl.Browse(ParentForm_=ic_user.icGetMainWin())
