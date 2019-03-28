#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель навигации тренда на базе утилиты gnuplot.
Абстрактный класс.
"""

import os
import os.path
import wx

from ic.components import icwidget
from ic.log import log
from ic.engine import panel_manager
from ic.dlg import ic_dlg
from ic.utils import printerfunc

from . import gnuplot_trend_navigator_panel_proto

# --- Спецификация ---
SPC_IC_NIXPLOT_TREND_NAVIGATOR = {
                                  'show_legend': False,
                                  '__parent__': icwidget.SPC_IC_WIDGET,
                                  '__attr_hlp__': {
                                                   'show_legend': u'Отображать легенду?',
                                                   },
                                  }

__version__ = (0, 1, 1, 1)

UNKNOWN_PEN_LABEL = u'Не определено разработчиком'

VIEW_REPORT_FILE_FMT = 'evince %s &'
# PRINT_REPORT_FILE_FMT = 'evince --preview %s &'


class icGnuplotTrendNavigatorProto(gnuplot_trend_navigator_panel_proto.icNixPlotTrendNavigatorPanelProto,
                                   panel_manager.icPanelManager):
    """
    Панель навигации тренда на базе утилиты gnuplot.
    Абстрактный класс.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        gnuplot_trend_navigator_panel_proto.icNixPlotTrendNavigatorPanelProto.__init__(self, *args, **kwargs)

        # Переключатель отображения легенды
        self.__is_show_legend = False

    def setIsShowLegend(self, is_show):
        """
        Установить переключатель отображения легенды.
        @param is_show: True - отобразить / False - скрыть
        @return:
        """
        self.__is_show_legend = is_show
        return self.showLegend(self.__is_show_legend)

    def draw(self, redraw=True):
        """
        Основной метод отрисовки тренда.
        @param redraw: Принудительная прорисовка.
        """
        return self.trend.draw(redraw)

    def getTrend(self):
        """
        Объект тренда.
        @return:
        """
        return self.trend

    def setLegend(self, pens=None):
        """
        Заполнить легенду.
        @param pens: Описания перьев.
        @return: True/False.
        """
        if pens is None:
            pens = self.trend.child

        # Очистить строки списка легенды
        self.legend_listBox.Clear()

        try:
            for pen in pens:
                pen_colour_rgb = pen.get('colour', (128, 128, 128))
                pen_label = pen.get('legend', UNKNOWN_PEN_LABEL)
                item = self.legend_listBox.Append(pen_label)
                if isinstance(pen_colour_rgb, tuple):
                    self.legend_listBox.SetItemForegroundColour(item, pen_colour_rgb)
                elif isinstance(pen_colour_rgb, str):
                    log.warning(u'Не поддерживается режим установки цвета')
            return True
        except:
            log.fatal(u'Ошибка заполнения легенды тренда')
        return False

    def showLegend(self, is_show=True):
        """
        Отобразить легенду?
        @param is_show: True - отобразить / False - скрыть
        @return: True/False.
        """
        self.__is_show_legend = is_show
        if is_show:
            result = self.expandSplitterPanel(splitter=self.trend_splitter, resize_panel=1)
        else:
            result = self.collapseSplitterPanel(splitter=self.trend_splitter, resize_panel=1)

        # self.Refresh()
        return result

    def onLegendButtonClick(self, event):
        """
        Обработчик включения/выключения легенды.
        """
        self.showLegend(not self.__is_show_legend)
        event.Skip()

    def onTrendSize(self, event):
        """
        Обработчик изменения контрола тренда.
        """
        width, height = self.getTrend().GetSize()
        log.debug(u'Перерисовка тренда [%d x %d]' % (width, height))
        self.getTrend().draw(size=(width, height))
        # self.showLegend(self.__is_show_legend)
        event.Skip()

    def onPrintButtonClick(self, event):
        """
        Обработчик кнопки печати тренда.
        """
        frame_filename = self.getReport()

        if frame_filename and os.path.exists(frame_filename):
            printerfunc.printPDF(frame_filename)

        event.Skip()

    def getReport(self):
        """
        Получить отчет в виде файла PDF.
        @return: Имя файла PDF или None в случае ошибки.
        """
        try:
            width, height = self.getTrend().GetSize()
            line_data = self.getTrend().getPenData()
            frame_filename = self.getTrend().report_frame(size=(width, height),
                                                          scene=self.getTrend().getCurScene(),
                                                          points=line_data)
            return frame_filename
        except:
            log.fatal(u'Ошибка получения отчета')
        return None

    def onViewButtonClick(self, event):
        """
        Обработчик кнопки просмотра отчета тренда.
        """
        frame_filename = self.getReport()

        if frame_filename and os.path.exists(frame_filename):
            cmd = VIEW_REPORT_FILE_FMT % frame_filename
            log.info(u'Выполнение комманды <%s>' % cmd)
            try:
                os.system(cmd)
            except:
                log.fatal(u'Ошибка выполнения комманды <%s>' % cmd)

        event.Skip()

    def onSettingsButtonClick(self, event):
        """
        Обработчик кнопки дополнительных настроек тренда.
        """
        ic_dlg.icWarningBox(u'НАСТРОЙКИ', u'Эта функция пока не реализована')
        event.Skip()

    def onUpButtonClick(self, event):
        """
        Передвижение сцены вверх.
        """
        self.getTrend().moveSceneY(step=1)
        event.Skip()

    def onDownButtonClick(self, event):
        """
        Передвижение сцены вниз.
        """
        self.getTrend().moveSceneY(step=-1)
        event.Skip()

    def onZoomInButtonClick(self, event):
        """
        Увеличение цены деления по Y.
        """
        self.getTrend().zoomY(step=1)
        event.Skip()

    def onZoomOutButtonClick(self, event):
        """
        Уменьшение цены деления по Y.
        """
        self.getTrend().zoomY(step=-1)
        event.Skip()

    def onFirstButtonClick(self, event):
        """
        Передвижение сцены к началу данных.
        """
        event.Skip()

    def onLastButtonClick(self, event):
        """
        Передвижение сцены к концу данных.
        """
        event.Skip()

    def onPrevButtonClick(self, event):
        """
        Передвижение сцены влево.
        """
        self.getTrend().moveSceneX(step=-1)
        event.Skip()

    def onNextButtonClick(self, event):
        """
        Передвижение сцены вправо.
        """
        self.getTrend().moveSceneX(step=1)
        event.Skip()

    def onTimeZoomInButtonClick(self, event):
        """
        Увеличение цены деления по временной шкале (шкала X).
        """
        self.getTrend().zoomX(step=1)
        event.Skip()

    def onTimeZoomOutButtonClick(self, event):
        """
        Уменьшение цены деления по временной шкале (шкала X).
        """
        self.getTrend().zoomX(step=-1)
        event.Skip()


def test():
    """
    Тестовая функция.
    """
    from ic import config

    log.init(config)

    app = wx.PySimpleApp()
    frame = wx.Frame(None, title='My Data')
    panel = icGnuplotTrendNavigatorProto(frame)
    panel.trend.draw()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    test()
