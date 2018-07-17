#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Импортер метаобъектов конфигурации 1с.
"""

# --- Imports ---
import os
import os.path
import copy

import wx
import wx.wizard

from . import about


__version__ = about.__version__
__date__ = about.__date__


# --- Classes ---
class icCFWizard(wx.wizard.Wizard):
    """
    Визард импортера метаобъектов конфигурации 1с.
    """
    def __init__(self, cf_filename=None):
        """
        Конструктор.
        @param cf_filename: Полное имя CF файла конфигурации.
        """
        if __file__:
            dir_name = os.path.dirname(__file__)
            if dir_name:
                path = os.path.dirname(__file__)
            else:
                path = os.getcwd()
        else:
            path = os.getcwd()
        img_file_name = os.path.join(path, 'img', '1c_wiz.png')
        self.wizard_img = wx.Image(img_file_name, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        
        title = u'Импорт метаобъектов конфигурации 1С: '
        if title:
            title += ' '+cf_filename
        wx.wizard.Wizard.__init__(self, None, -1, title, self.wizard_img)
        
        # Список порядка следования страниц
        self.page_order = []
        
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_changed)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.on_changing)
        
        # Внутренне окружение визарда инсталяции
        self.environment = {}
        self._init_env(cf_filename=cf_filename)
        
    def getPage(self, idx):
        """
        Получить страницу по индексу.
        """
        return self.page_order[idx]
        
    def getFinishPage(self):
        """
        Последняя финишная страница.
        """
        return self.getPage(-1)
        
    def appendPage(self, page):
        """
        Установка следующей страницы.
        """
        if page:
            if self.page_order:
                # Установить связи между страницами
                page.SetPrev(self.page_order[-1])
                self.page_order[-1].SetNext(page)
            self.page_order.append(page)

    def getNextPage(self, page):
        """
        Получить следующую страницу за указанной.
        """
        if page:
            if self.page_order:
                i = self.page_order.index(page)
                if i < len(self.page_order)-1:
                    return self.page_order[i+1]
                else:
                    return None
                
    def on_changed(self, event):
        """
        Обработчик смены страницы инсталляции.
        Это обработчик срабатывает перед 
        появлением страницы на экране. См. демку.
        """
        page = event.GetPage()
        if hasattr(page, 'on_changed'):
            return page.on_changed(event)
        event.Skip()

    def on_changing(self, event):
        """
        Обработчик смены страницы инсталляции.
        Это обработчик срабатывает после 
        нажатия на кнопку Next.
        """
        page = event.GetPage()
        if hasattr(page, 'on_changing'):
            return page.on_changing(event)
        event.Skip()
        
    def runFirstPage(self):
        """
        Запуск первой страницы.
        """
        if self.page_order:
            first_page = self.page_order[0]
            if first_page:
                self.RunWizard(first_page)
                
    def _init_env(self, **kwargs):
        """
        Инициализация внутреннего окружения визарда.
        """
        from . import iccfanalyzer

        self.environment = copy.deepcopy(kwargs)
        
        self.environment['cf_analyzer'] = iccfanalyzer.icCFAnalyzer()

    def getCFAnalyzer(self):
        """
        Объект анализатора конфигурации.
        """
        return self.environment['cf_analyzer']


def run_wizard(*args, **kwargs):
    """
    Запуск визарда. Запуск производиться без создания объекта приложения.
    Функция может быть вызвана из другой программы.
    """
    from . import icWizardPages

    wizard = icCFWizard(u'Версия %s от %s' % ('.'.join([str(i) for i in __version__]), __date__))

    page1 = icWizardPages.icCFParsePage(wizard, u'Парсинг конфигурации 1с')
    wizard.appendPage(page1)

    page2 = icWizardPages.icCFChoicePage(wizard, u'Выбор объектов конфигурации')
    wizard.appendPage(page2)

    page_end = icWizardPages.icCFEndPage(wizard, u'Окончание', u'''Изменение конфигурации 1с успешно завершено''')
    wizard.appendPage(page_end)

    wizard.FitToPage(page1)

    wizard.RunWizard(page1)


def run(*args, **kwargs):
    """
    Основная функция запуска визарда.
    Запуск производиться с создание объекта приложения.
    Функция вызывается для автономного использования.
    """
    app = wx.PySimpleApp()
    run_wizard(*args, **kwargs)


def test():
    """
    Функция тестирования визарда инсталятора.
    """
    run()


if __name__ == '__main__':
    test()
