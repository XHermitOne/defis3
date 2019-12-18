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
from ic.engine import form_manager
from ic.dlg import dlgfunc
from ic.utils import printerfunc

from . import gnuplot_trend_navigator_panel_proto

# --- Спецификация ---
SPC_IC_GNUPLOT_TREND_NAVIGATOR = {
                                  'show_legend': True,
                                  '__parent__': icwidget.SPC_IC_WIDGET,
                                  '__attr_hlp__': {
                                                   'show_legend': u'Отображать легенду?',
                                                   },
                                  }

__version__ = (0, 1, 3, 1)

UNKNOWN_PEN_LABEL = u'Не определено разработчиком'

VIEW_REPORT_FILE_FMT = 'evince %s &'
# PRINT_REPORT_FILE_FMT = 'evince --preview %s &'


class icGnuplotTrendNavigatorProto(gnuplot_trend_navigator_panel_proto.icGnuplotTrendNavigatorPanelProto,
                                   form_manager.icFormManager):
    """
    Панель навигации тренда на базе утилиты gnuplot.
    Абстрактный класс.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор.
        """
        gnuplot_trend_navigator_panel_proto.icGnuplotTrendNavigatorPanelProto.__init__(self, *args, **kwargs)

        # Должна быть хотя бы одна колонка у легенды
        self.setColumns_list_ctrl(ctrl=self.legend_listCtrl,
                                  cols=(dict(label=u'', width=self.legend_listCtrl.GetSize().GetWidth()), ))

        # Переключатель отображения легенды
        self.__is_show_legend = False

    def setIsShowLegend(self, is_show):
        """
        Установить переключатель отображения легенды.

        :param is_show: True - отобразить / False - скрыть
        :return:
        """
        return self.showLegend(is_show)

    def draw(self, redraw=True):
        """
        Основной метод отрисовки тренда.

        :param redraw: Принудительная прорисовка.
        """
        return self.trend.draw(redraw)

    def getTrend(self):
        """
        Объект тренда.

        :return:
        """
        return self.trend

    def setStartDT(self, new_dt):
        """
        Начальная дата-время тренда.

        :param new_dt: Новое значение.
        """
        return self.trend.setStartDT(new_dt=new_dt)

    def setStopDT(self, new_dt):
        """
        Конечная дата-время тренда.

        :param new_dt: Новое значение.
        """
        return self.trend.setStopDT(new_dt=new_dt)

    def getStartDT(self):
        """
        Начальная дата-время тренда.
        """
        return self.trend.getStartDT()

    def getStopDT(self):
        """
        Конечная дата-время тренда.
        """
        return self.trend.getStopDT()

    def getPenData(self, pen_index=0):
        """
        Данные соответствующие перу.

        :param pen_index: Индекс пера. По умолчанию берется первое перо.
        :return: Список (Время, Значение)
        """
        return self.trend.getPenData(pen_index=pen_index)

    def setLegend(self, pens=None):
        """
        Заполнить легенду.

        :param pens: Описания перьев.
        :return: True/False.
        """
        if pens is None:
            pens = self.trend.child

        # Очистить строки списка легенды
        self.clear_list_ctrl(ctrl=self.legend_listCtrl)

        try:
            for pen in pens:
                pen_colour_rgb = pen.get('colour', (128, 128, 128))
                # Определяем надпись пера в легенде
                pen_label = pen.get('legend', UNKNOWN_PEN_LABEL)
                pen_label = pen_label if pen_label else str(pen.get('description', UNKNOWN_PEN_LABEL))
                self.appendRow_list_ctrl(ctrl=self.legend_listCtrl, row=(pen_label, ))

                row = self.getItemCount(self.legend_listCtrl) - 1
                if isinstance(pen_colour_rgb, tuple) or isinstance(pen_colour_rgb, wx.Colour):
                    self.setRowForegroundColour_list_ctrl(ctrl=self.legend_listCtrl,
                                                          i_row=row, colour=pen_colour_rgb)
                elif isinstance(pen_colour_rgb, str):
                    self.setRowForegroundColour_list_ctrl(ctrl=self.legend_listCtrl,
                                                          i_row=row, colour=wx.Colour(pen_colour_rgb))
                else:
                    log.warning(u'Не поддерживается режим установки цвета')
            return True
        except:
            log.fatal(u'Ошибка заполнения легенды тренда')
        return False

    def showLegend(self, is_show=True, redraw=True):
        """
        Отобразить легенду?

        :param is_show: True - отобразить / False - скрыть
        :param redraw: Перерисовка сплиттера.
        :return: True/False.
        """
        self.__is_show_legend = is_show
        if is_show:
            result = self.expandSplitterPanel(splitter=self.trend_splitter, redraw=redraw)
        else:
            result = self.collapseSplitterPanel(splitter=self.trend_splitter, redraw=redraw)

        # if redraw:
        #     self.trend_splitter.Refresh()
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

        :return: Имя файла PDF или None в случае ошибки.
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
            log.info(u'Выполнение команды <%s>' % cmd)
            try:
                os.system(cmd)
            except:
                log.fatal(u'Ошибка выполнения команды <%s>' % cmd)

        event.Skip()

    def onSettingsButtonClick(self, event):
        """
        Обработчик кнопки дополнительных настроек тренда.
        """
        dlgfunc.openWarningBox(u'НАСТРОЙКИ', u'Эта функция пока не реализована')
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
        Масштабирование. Увеличение.
        """
        self.getTrend().zoomY(step=-1)
        event.Skip()

    def onZoomOutButtonClick(self, event):
        """
        Масштабирование. Уменьшение.
        """
        self.getTrend().zoomY(step=1)
        event.Skip()

    def onFirstButtonClick(self, event):
        """
        Передвижение сцены к началу данных.
        """
        self.getTrend().moveSceneFirst()
        event.Skip()

    def onLastButtonClick(self, event):
        """
        Передвижение сцены к концу данных.
        """
        self.getTrend().moveSceneLast()
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
        Масштабирование. Увеличение по временной шкале (шкала X).
        """
        self.getTrend().zoomX(step=-1)
        event.Skip()

    def onTimeZoomOutButtonClick(self, event):
        """
        Масштабирование. Уменьшение по временной шкале (шкала X).
        """
        self.getTrend().zoomX(step=1)
        event.Skip()

    # def onNavigatorSize(self, event):
    #     """
    #     Изменение размера панели навигатора.
    #     """
    #     self.showLegend(self.__is_show_legend)
    #     event.Skip()


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
