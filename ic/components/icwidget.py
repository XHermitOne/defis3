#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Базовые кдассы библиотеки от которых наследуются все остальные.
Содержит описание базовых классов всех компонентов библиотеки ic: icBase, icSizer, icWidget.
@type SPC_IC_SIMPLE: C{dictionary}
@var SPC_IC_SIMPLE: Спецификация на ресурсное описание базового класса. Описание ключей SPC_IC_SIMPLE:

    - B{name='simple'}: Имя окна.
    - B{type='Simple'}: Тип объекта.
    - B{alias=None}: Алиасное имя.
    - B{activate=1}: Выражение на активацию. Если оно возвращает True, то
        компонент создается, в противном случае нет.
    - B{style=0}:Стиль компонента.
    - B{init_expr=None}: Выражение, вычисляемое после создания компонента.
    - B{component_module=None}: Модуль, где хранится описание компонента (класса обкладки)
        ; если он не определен, то используется стандартный класс. Имя класс
        должно соответствовать типу компонента (стандартные классы начинаются с 'ic');
        параметрами конструктора должны быть стандартные параметры конструекторов
        системных компонентов;
        component_module.<type>.(parent, id=-1, component=None, logType = 0, evalSpace = None).
    - B{res_module=None}: Имя модуля ресурса (+обработчики событий).
    - B{obj_module=None}: Имя модуля объекта.
    - B{data_name=None}: Имя данных из контекста для инициализации объекта.
    - B{__default_page__=0}: Номер страницы в редакторе ресурсов открываемой в первую очередь.
    - B{__loaded_res_module=None}: Импортированный модуль ресурса.
    - B{__loaded_obj_module=None}: Импортированный модуль объекта.
    - B{_uuid=None}: Универсальный уникальный идентификатор ресурсного описания.
    - B{__interface__=None}: Имя интерфейса, куда входит компонент. Позволяет обращатся
        из вычисляемого атрибута к данному интерфейсу через функцию GetInterface()
        (см. описание ic.kernel.icContext.Context). Интерфейс является объектом
        (наследнуемый от icTemplateInterface), который агрегирует в себе другие
        компоненты и предоставляе специальный интерфейс достуа к ним. Используется для
        управления сложными составными компонентами (подробнее см. документацию).
    - B{__styles__}: Указатель на словарь стилей.
    - B{__lists__}: Указатель на словарь списков возможных значений некоторых атрибутов.
    - B{__doc__=None}: Имя файла документации из папки ic/doc/public на данный компонент.
        Пример: ic.components.user.icspravtreelist.SpravTreeList-class.html.
    - B{__attr_types__=None}: Описание типов атрибутов в виде словаря. В
        качестве ключей идентификаторы типов (идентификаторы описаны в модуле
        ic.PropertyEditor.icDefInf.py),в качестве значений список
        атрибитов данного типа.
    - B{__item_id}: Уникальный идентификатор описания.
    - B{__version__base='0.0.0.0'}: Версия базовой спецификации объекта.
    - B{__version__='0.0.0.0'}: Версия спецификации объекта.

@type SPC_IC_BASE: C{dictionary}
@var SPC_IC_BASE: Спецификация на ресурсное описание базового класса. Описание ключей SPC_IC_BASE:

    - B{name='widget'}: Имя окна.
    - B{type='Widget'}: Тип объекта.
    - B{span=(1,1)}: Параметр объеденения ячеек в сайзере GridBoxSizer.
    - B{proportion=0}: Параметр пропорциональности при добавлении в сайзер.
    - B{flag=0}: Параметр flag при добавлении в сайзер.
    - B{border=0}: Признак признак бордюры при добавлении в сайзер.

@type SPC_IC_SIZER: C{dictionary}
@var SPC_IC_SIZER: Спецификация на ресурсное описание базового класса сайзеров. Описание ключей SPC_IC_SIZER:

    - B{name='DefaultName'}:Имя окна.
    - B{type='Sizer'}: Тип объекта.
    - B{vgap=0}: Отступы между рядами.
    - B{hgap=0}: Отступы между колонками.
    - B{__parent__=SPC_IC_BASE}: Спецификация, от которой происходит наследование аттрибутов.
    - B{child=[]}:

@type SPC_IC_WIDGET: C{dictionary}
@var SPC_IC_WIDGET: Спецификация на ресурсное описание базового класса визуальных компонентов.
Описание ключей SPC_IC_WIDGET:

    - B{name='widget'}: Имя окна.
    - B{type='Widget'}: Тип объекта.
    - B{__version__icwidget='0.0.0.0'}: Версия базовой спецификации визуальных объектов.
    - B{alias=None}: Алиасное имя.
    - B{position=(-1,-1)}: Расположение на родительском окне.
    - B{size=(-1,-1)}: Размер компонента.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{moveAfterInTabOrder=''}: Имя компонента в очереди переходов по TAB,
        после которого текущий компонент должен быть помещен.
    - B{style=0}: Стиль компонента.
    - B{activate=1}: Выражение на активацию. Если оно возвращает True, то
        компонент создается, в противном случае нет.
    - B{show=1}: Признак визуализации.
    - B{refresh=None}: Список компонентов, которые обновляются при изменении
        компонента.
    - B{recount=None}: Список компонентов, которые пересчитывают значения при
        изменении компонента.
    - B{proportion=0}: Параметр пропорциональности.
    - B{flag=0}: Параметр flag при добавлении в сайзер.
    - B{border=0}: Признак признак бордюры.
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки в компоненте.
    - B{onInit=None}: Выражение, выполняемое при обработки сообщения <icEvents.EVT_POST_INIT>;
        сообющение посылается всем компонентам формы после ее создания.
    - B{source=None}: Имя объекта данных (icSQLObjDataset) с которым работает компонент.
    - B{__events__=None}: Описание обработчиков событий. Ключи - атрибуты, которые являются
        обработчиками событий, значения - описательная структура события.
    - B{__parent__=SPC_IC_BASE}: Спецификация, от которой происходит наследование аттрибутов.
"""

import os
import wx

import ic.PropertyEditor.icDefInf as icDefInf
from . import icEvents
import ic.utils.graphicUtils as graphicUtils
import ic.utils.resource as resource
import ic.utils.util as util
from ic.utils import ic_uuid
from ic.log import log
from . import icEvents
import ic.dlg.msgbox as msg
import ic.kernel.icobject as icobject
import ic.kernel.icContext as icContext
import ic.kernel.icsignalsrc as icsignalsrc
import ic.kernel.io_prnt as io_prnt
import ic


SPC_IC_SIMPLE = {'name': 'base',
                 'type': 'Base',
                 'alias': None,
                 'activate': True,
                 'style': 0,
                 'init_expr': None,
                 'component_module': None,
                 'res_module': None,
                 'obj_module': None,
                 'description': None,
                 'data_name': None,     # Имя данных из контекста
                 '_uuid': None,
                 '__default_page__': 0,
                 '__styles__': None,
                 '__interface__': None,
                 '__brief_attrs__': [],     # Список атрибутов, которые будут видны в дереве через ":"
                 '__doc__': None,
                 '__item_id': None,
                 '__version__base': '0.0.0.0',
                 '__version__': '0.0.0.0',
                 '__init_res_by_wizard__': None,
                 '__attr_types__': {icDefInf.EDT_PY_SCRIPT: ['init_expr', 'pre_init_expr', 'description'],
                                    icDefInf.EDT_TEXTFIELD: ['name', 'type', 'alias', 'data_name'],
                                    icDefInf.EDT_RO_TEXTFIELD: ['res_module', '_uuid', 'obj_module'],
                                    icDefInf.EDT_COMBINE: ['style'],
                                    icDefInf.EDT_CHECK_BOX: ['activate'],
                                    },
                 '__attr_hlp__': {'name': u'Имя объекта',
                                  'type': u'Тип объекта',
                                  'activate': u'Вкл./Выкл. создание объекта',
                                  'data_name': u'Имя данных из контекста',
                                  'description': u'Описание',
                                  'style': u'Стиль компонента',
                                  'init_expr': u'Выражение, выполняемой при инициализации компонента',
                                  'component_module': u'Модуль компонента',
                                  'res_module': u'Модуль ресурса',
                                  'obj_module': u'Модуль объекта',
                                  },
                 }

SPC_IC_BASE = {'name': 'base',
               'type': 'Base',
               'size': (-1, -1),
               'position': (-1, -1),
               'span': (1, 1),
               'proportion': 1,
               'flag': wx.GROW | wx.EXPAND,
               'border': 5,
               '__attr_types__': {icDefInf.EDT_POINT: ['position', 'span'],
                                  icDefInf.EDT_SIZE: ['size'],
                                  icDefInf.EDT_COMBINE: ['flag'],
                                  icDefInf.EDT_NUMBER: ['border', 'proportion'],
                                  icDefInf.EDT_CHOICE: ['layout', 'alignment']},
               '__lists__': {'layout': ['vertical', 'horizontal'],
                             'alignment': ['(\'left\', \'middle\')',
                                           '(\'left\', \'top\')',
                                           '(\'left\', \'bottom\')',
                                           '(\'centred\', \'middle\')',
                                           '(\'centred\', \'top\')',
                                           '(\'centred\', \'bottom\')',
                                           '(\'right\', \'middle\')',
                                           '(\'right\', \'top\')',
                                           '(\'right\', \'bottom\')']},
               '__parent__': SPC_IC_SIMPLE,
               '__attr_hlp__': {'size': u'Размер объекта',
                                'position': u'Позиция',
                                'span': u'Определяет сколько ячеек по горизонтали и вертикали должен занимать компонент',
                                'proportion': u'Признак пропорционального размера',
                                'flag': u'Флаг размещения',
                                'border': u'Величина отступа вокруг компонента',
                                }
               }

SPC_IC_WIDGET = {'name': 'widget',
                 'type': 'Widget',
                 'foregroundColor': None,
                 'backgroundColor': None,
                 'show': 1,
                 'refresh': None,
                 'enable': True,
                 'recount': None,
                 'source': None,
                 'keyDown': None,
                 'onInit': None,
                 'moveAfterInTabOrder': '',
                 '__events__': {'keyDown': ('wx.EVT_KEY_DOWN', 'OnKeyDown', False),
                                'onInit': ('icEvents.EVT_POST_INIT', 'OnInit', False)},
                 '__version__icwidget': '0.0.0.0',
                 '__attr_types__': {icDefInf.EDT_TEXTFIELD: ['moveAfterInTabOrder', 'field_name', 'label'],
                                    icDefInf.EDT_PY_SCRIPT: ['show', 'refresh', 'recount', 'source', 'keyDown'],
                                    icDefInf.EDT_COLOR: ['foregroundColor', 'backgroundColor'],
                                    icDefInf.EDT_CHECK_BOX: ['enable'],
                                    icDefInf.EDT_FONT: ['font']},
                 '__parent__': SPC_IC_BASE,
                 '__attr_hlp__': {'foregroundColor': u'Цвет текста',
                                  'backgroundColor': u'Цвет фона',
                                  'show': u'Признак видимости',
                                  'enable': u'Вкл./Выкл. объект',
                                  'onInit': u'Обработчик инициализации объекта',
                                  'keyDown': u'Обработчик нажатия кнопки клавиатуры',
                                  },
                 }

SPC_IC_SIZER = {'name': 'DefaultName',
                'type': 'Sizer',
                'vgap': 0,
                'hgap': 0,
                'position': (0, 0),
                'span': (1, 1),
                'child': [],

                '__attr_types__': {icDefInf.EDT_NUMBER: ['vgap, hgap'],
                                   icDefInf.EDT_CHOICE: ['layout', 'alignment']},
                '__parent__': SPC_IC_BASE,
                '__attr_hlp__': {'vgap': u'Величина зазора между соседними ячейками по вертикали',
                                 'hgap': u'Величина зазора между соседними ячейками по горизонтали',
                                 'position': u'Позиция',
                                 'span': u'Определяет сколько ячеек по горизонтали и вертикали должен занимать компонент',
                                 },
                }


_ = wx.GetTranslation

__version__ = (1, 0, 4, 6)

#   Указатель на окно всплывающей подсказки
icHelpStringWin = None


def getHelpStringWin():
    """
    Возвращает указатель на окно всплывающей подсказки.
    """
    global icHelpStringWin
    return icHelpStringWin


def setHelpStringWin(win):
    """
    Возвращает указатель на окно всплывающей подсказки.
    """
    global icHelpStringWin
    icHelpStringWin = win

#   Типы редактируемый представлений компонентов
#   Текущий выбранный компонент
icSelectedShapeType = 1
#   Родительский компонент
icParentShapeType = 2
#   Реальное представление компонента
icRealShapeType = 0

#   Переменные и функции поддержки уникальных идентификаторов визуальных объектов
#   системы
icIdCount = 1000
#   Переменные и функции поддержки уникальных идентификаторов визуальных объектов
#   формы
icIdCountForm = 1000


def setIdBeginValue(val=1000):
    global icIdCountForm
    icIdCountForm = val


def icNextId():
    """
    Генерирует следующее значение идентификатора.
    """
    global icIdCount
    icIdCount += 1
    return icIdCount


def icNewId():
    """
    Функция генерирует идентификаторы для компонентов. Отличие от функции
    icNextId в том, что она возвращает -1, если счетчик выходит за пределы 32767.
    """
    global icIdCountForm
    icIdCountForm += 1

    if icIdCountForm > 32767:
        return -1

    return icIdCountForm


class icShape:
    """
    Базовый класс для всех визуальных компонентов, описывает представление
    компонента в графическом редакторе форм.
    """

    def __init__(self, parent, id,  component=None, logType = 0, evalSpace = None):
        """
        Конструктор.
        """
        #   Тип текущего предстваления компонента
        self.shapeType = 0
        #   Указатель на подложку редактора
        self.editorBackground = None
        #   Флаг, разрешающий перетаскивать компонент
        self.SetFlagMove()
        #   Флаг, разрешающий менять размер компонента
        self.SetFlagResize()
        #   Отступ от краев при рисовании курсора
        self.cursorBorder = 0

    def CanMoveObj(self):
        """
        Функция возвращает значение флага, разрещающего перемещать объект.
        """
        return self.bMoveObj

    def SetFlagMove(self, flag=True):
        """
        Функция устанавливает значение флага, разрещающего перемещать
        объект.
        """
        self.bMoveObj = flag

    def CanResizeObj(self):
        """
        Функция возвращает значение флага, разрещающего изменять размер
        объекта.
        """
        return self.bResizeObj

    def SetFlagResize(self, flag=True):
        """
        Функция устанавливает значение флага, разрещающего изменять размер
        объекта.
        """
        self.bResizeObj = flag

    def SetSelected(self):
        """
        устанавливает объект в качестве текущего.
        """
        self.shapeType = icSelectedShapeType

    def GetShapeType(self):
        """
        Возвращает тип формы.
        """
        return self.shapeType

    def SetShapeType(self, type=icRealShapeType):
        """
        Устанавливает тип формы.
        """
        self.shapeType = type

    def EraseCursor(self, dc=None):
        """
        Удаляет курсор.
        """
        if self.editorBackground:
            try:
                self.DrawCursor(dc, self.GetParent().GetBackgroundColour())
            except:
                pass

    def DrawCursor(self, dc=None, clr=(0, 0, 0)):
        """
        Рисует курсор.
        """
        if not dc:
            dc = wx.ClientDC(self.GetParent())

        x, y = self.GetPosition()
        sx, sy = self.GetSize()
        x, y = x + self.cursorBorder, y + self.cursorBorder
        sx, sy = sx - 2*self.cursorBorder, sy - 2*self.cursorBorder

        oldpen = dc.GetPen()
        oldbrush = dc.GetBrush()
        pen = wx.Pen(clr, 1)
        brush = wx.Brush(clr)

        #   Рисуем курсор
        dc.SetBrush(brush)
        dc.SetPen(pen)
        dc.DrawLines([(1, 1), (sx, 1), (sx, sy), (1, sy), (1, 1)], x-1, y-1)
        #   По необходимости рисуем маркеры для изменения размеров объекта
        if self.CanResizeObj():
            pen = wx.Pen(clr)
            dc.SetPen(pen)

            szm = 4
            dc.DrawRectangle(x-2 - szm/2, y-2-szm/2, szm, szm)
            dc.DrawRectangle(x - szm/2 + sx+2, y-2-szm/2, szm, szm)
            dc.DrawRectangle(x - szm/2 + sx+2, y-szm/2 + sy+2, szm, szm)
            dc.DrawRectangle(x-2 - szm/2, y-szm/2 + sy+2, szm, szm)

        #   Востанавливаем
        dc.SetBrush(oldbrush)
        dc.SetPen(oldpen)

    def SetEditorMode(self):
        """
        Устанавливает режим редактора.
        """
        self.is_editor_mode = True

    def DrawShape(self, dc=None):
        """
        Функция перерисовывает компонент.
        @type dc: C{wx.DC}
        @param dc: Контекст устроийства вывода.
        """
        #   Вызываем метод перерисовки компонента
        if self.editorBackground:
            if self.shapeType == icParentShapeType:
                self.DrawCursor(clr=(190, 0, 0))
            elif self.shapeType == icSelectedShapeType:
                self.DrawCursor()

msgEvalAttrError = ''' eval_attr(...)
###########################################################
#### EVAL ATTRIBUTE Error in component=%s,
####                         attribute=%s
#### <UUID = %s>
###########################################################
'''


class icResObjContext(icContext.Context):
    """
    Контекст объектов, создаваемых по ресурсному описанию.
    """

    def __init__(self, *args, **kwargs):
        """
        Конструктор
        """
        icContext.Context.__init__(self, *args, **kwargs)

        # Список обработанных контролов (используется только внутри класса)
        self._controls_ = []

    def init_serv_context(self):
        """
        Инициализация сервесных ключей.
        """
        icContext.Context.init_serv_context(self)
        # Основные ключи, используемые в прошлых версиях системы
        #   Параметры формы
        self['_form_param'] = {}
        #   Признак блокировки сообщений от клавиатуры
        self['__block_key_down'] = False
        #   Признак запрещающий блокировки записей
        self['__block_lock_rec'] = False
        #   Режим работы компонента
        self['__runtime_mode'] = 0
        #   Содержит описание параметров последней вызванной функции
        self['_lfp'] = {}
        #   Ссылка на пространство имен <Осталось для совместимости>
        self['_esp'] = self

    def init_context(self):
        """
        Инициализируем контекст ресурсных объектов.
        """
        icprs, icres, common = util.init_eval_space_modules()
        self.setKey('CreateForm', icprs.CreateForm)
        self.setKey('ResultForm', icprs.ResultForm)
        self.setKey('ModalForm', icprs.ModalForm)
        self.setKey('method', icres.method)
        self.setKey('wx', wx)
        self.setKey('ic', ic)
        self.setKey('_', wx.GetTranslation)
        self.setKey('icImageLibName', common.icImageLibName)
        self.setKey('imglib', common)
        #   Имя модуля ресурса
        self.setKey('res_module', None)
        #   Имя файла ресурса
        self['__file_res'] = None
        #   Стандартное имя обработчика событий
        self.setKey('evt', None)

    def setValueInCtrl(self, Control_, DataDict_):
        """
        Установить значения контролов из словаря.
        @param Control_: Обрабатываемая форма/контрол.
        """
        self._controls_ = []
        result = self._setValueInCtrl(Control_, DataDict_)
        # После работы с контролами сбросить список обработанных контролов
        self._controls_ = []
        return result

    def _setValueInCtrl(self, Control_, DataDict_):
        """
        Установить значения контролов в форме из словаря.
        @param Control_: Обрабатываемая форма/контрол.
        """
        # Инициализировать значения всех контролов
        if DataDict_:
            data_names = DataDict_.keys()
            for ctrl in Control_.get_children_lst():
                try:
                    # Проверить обрабатывался ли уже контрол
                    if ctrl in self._controls_:
                        # Если да то пропустить обработку
                        continue
                    else:
                        # Если нет, то обработать
                        self._controls_.append(ctrl)

                    if 'data_name' in ctrl.resource:
                        data_name = ctrl.resource['data_name']
                        if data_name and data_name in data_names:
                            value = DataDict_[data_name]
                            self._setCtrlValue(ctrl, value,
                                               u'Ошибка инициализации контрола <%s> значением  <%s>' % (ctrl.name, data_name))

                    # Внимание! Контрол может принимать значения из нескольких
                    # полей. Эта функция включается только у тех контролов
                    # у которых это необходимо.
                    if 'data_names' in ctrl.resource:
                        data_name_lst = ctrl.resource['data_names']
                        if data_name_lst:
                            values = []
                            for data_name in data_name_lst:
                                if data_name and data_name in data_names:
                                    value = DataDict_[data_name]
                                    values.append(value)
                            self._setCtrlValue(ctrl, values,
                                               u'Ошибка инициализации контрола <%s> значением  <%s>' % (ctrl.name, data_name_lst))
                    
                    # Обработать дочерние элементы
                    is_ctrl_children = bool(ctrl.get_children_lst())
                    if is_ctrl_children:
                        self._setValueInCtrl(ctrl, DataDict_)
                except wx.PyDeadObjectError:
                    io_prnt.outErr(u'Обращение к разрушенному wx объекту')

    def _setCtrlValue(self, Control_, Value_=None, ErrMsg_=u''):
        """
        Функция установки значения контрола с обработкой ошибки.
        @param Control_: Объект контрола.
        @param Value_: Устанавливаемое значение.
        @param ErrMsg_: Сообщение в случае ошибки.
        """
        try:
            if Value_ is None:
                Value_ = ''
            Control_.setValue(Value_)
        except:
            io_prnt.outErr(ErrMsg_)
        
    def clearValueInCtrl(self, Control_, DataNames_=None):
        """
        Сбросить значения контролов.
        @param Control_: Обрабатываемая форма/контрол.
        @param DataNames_: Список имен, для контролов которых
        нужно сбросить значения. Если None, то сбрасываются
        значения у всех контролов.
        """
        self._controls_ = []
        self._clearValueInCtrl(Control_, DataNames_)
        # После работы с контролами сбросить список обработанных контролов
        self._controls_ = []

    def _clearValueInCtrl(self, Control_, DataNames_=None):
        """
        Ссбросить значения контролов в форме.
        @param Control_: Обрабатываемая форма/контрол.
        @param DataNames_: Список имен, для контролов которых
        нужно сбросить значения. Если None, то сбрасываются
        значения у всех контролов.
        """
        # Инициализировать значения всех контролов
        for ctrl in Control_.get_children_lst():
            try:
                # Проверить обрабатывался ли уже контрол
                if ctrl in self._controls_:
                    # Если да то пропустить обработку
                    continue
                else:
                    # Если нет, то обработать
                    self._controls_.append(ctrl)

                if 'data_name' in ctrl.resource:
                    data_name=ctrl.resource['data_name']
                    if DataNames_:
                        if data_name and data_name in DataNames_:
                            self._setCtrlValue(ctrl, None,
                                               u'Ошибка инициализации контрола <%s> значением  <%s>' % (ctrl.name, data_name))
                    else:
                        self._setCtrlValue(ctrl, None,
                                           u'Ошибка инициализации контрола <%s> значением  <%s>' % (ctrl.name, data_name))
                    
                # Внимание! Контрол может принимать значения из нескольких
                # полей. Эта функция включается только у тех контролов
                # у которых это необходимо.
                if 'data_names' in ctrl.resource:
                    data_name_lst = ctrl.resource['data_names']
                    if DataNames_ and data_name_lst:
                        result = False
                        for data_name in data_name_lst:
                            if data_name and data_name in DataNames_:
                                # Если хотябы одно поле из имеющихся чистое
                                # то очищается значение контрола
                                result = True
                                break
                        if result:
                            self._setCtrlValue(ctrl, None,
                                               u'Ошибка инициализации контрола <%s> значением  <%s>' % (ctrl.name, data_name_lst))
                        
                # Обработать дочерние элементы
                is_ctrl_children = bool(ctrl.get_children_lst())
                if is_ctrl_children:
                    self._clearValueInCtrl(ctrl, DataNames_)
            except wx.PyDeadObjectError:
                io_prnt.outErr(u'Обращение к разрушенному wx объекту')

    def FindObject(self, type_=None, name=None):
        return icContext.Context.FindObject(self, type_, name)

    def getValueInCtrl(self, Control_):
        """
        Получить значения контролов в виде словаря.
        @param Control_: Обрабатываемая форма/контрол.
        """
        self._controls_ = []
        result = self._getValueInCtrl(Control_)
        # После работы с контролами формы сбросить список обработанных контролов
        self._controls_ = []
        return result

    def _getValueInCtrl(self, Control_):
        """
        Получить значения контролов в форме в виде словаря.
        @param Control_: Обрабатываемая форма/контрол.
        """
        data = {}
        # Инициализировать значения всех контролов
        for ctrl in Control_.get_children_lst():
            try:
                # Проверить обрабатывался ли уже контрол
                if ctrl in self._controls_:
                    # Если да то пропустить обработку
                    continue
                else:
                    # Если нет, то обработать
                    self._controls_.append(ctrl)

                if 'data_name' in ctrl.resource:
                    data_name = ctrl.resource['data_name']
                    if data_name:
                        try:
                            data[data_name] = ctrl.getValue()
                        except:
                            io_prnt.outErr(u'Ошибка чтения значения контрола %s' % ctrl.name)
                # Внимание! Контрол может принимать значения из нескольких
                # полей. Эта функция включается только у тех контролов
                # у которых это необходимо.
                if 'data_names' in ctrl.resource:
                    data_name_lst = ctrl.resource['data_names']
                    if data_name_lst:
                        try:
                            values = ctrl.getValue()
                            for i, data_name in enumerate(data_name_lst):
                                data[data_name] = values[i]
                        except:
                            io_prnt.outErr(u'Ошибка чтения значения контрола %s' % ctrl.name)
                            
                # Обработать дочерние элементы
                is_ctrl_children = bool(ctrl.get_children_lst())
                if is_ctrl_children:
                    child_data = self._getValueInCtrl(ctrl)
                    data.update(child_data)
            except wx.PyDeadObjectError:
                io_prnt.outErr(u'Обращение к разрушенному wx объекту')
        return data


class icSimple(icobject.icObject):
    """
    Базовый класс для всех компонентов библиотеки ic, работающих с
    ресурсными описаниями.
    """

    @staticmethod
    def GetEditorResourceManager():
        """
        Указатель на класс управления ресурсом в редакторе ресурсов.
        """
        return None
    
    @staticmethod
    def GetDesigner():
        """
        Указатель на класс графического редактора компонента.
        """
        return None

    @staticmethod
    def TestComponentResource(res, context, parent=None, *arg, **kwarg):
        """
        Функция тестирования компонента.
        @param res: Ресурсное описание.
        @param context: Контекст ресурса.
        @param parent: Родительское окно.
        """
        return None

    def __init__(self, parent, id=-1, component=None, logType=0,
                 evalSpace=None, bGenUUID=True, bPrepareProp=False):
        """
        Конструктор для создания icBase.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """
        if id > 32767:
            id = -1
        elif id < 0:
            id = -1

        if evalSpace is None:
            evalSpace = icResObjContext(resource.icGetKernel())
        elif isinstance(evalSpace, dict):
            space_dict = evalSpace
            evalSpace = icResObjContext(resource.icGetKernel())
            evalSpace.update(space_dict)
        elif not evalSpace.get_kernel():
            evalSpace.kernel = resource.icGetKernel()

        component = util.icSpcDefStruct(SPC_IC_SIMPLE, component)
        self.resource = component
        if bPrepareProp:
            self.set_resource_property()
        #   Определяем имя интерфейса, если он есть
        if '__interface__' in component:
            self.__interface = component['__interface__']
        else:
            self.__interface = None
        #   Вызываем конструктор
        icobject.icObject.__init__(self, component['name'], icNextId(),
                                   context=evalSpace, cmpInterface=self.__interface, typ=component['type'])
        self.parent = parent
        self.logType = logType
        self.description = component['description']
        self.style = component['style']
        self.component_module = component['component_module']
        self.res_module = component['res_module']

        if 'child' in component:
            self.child = component['child']
        else:
            self.child = None

        #   Структуры, где регистрируются дочерние компонеты
        self.components = {}
        self.component_lst = []
        #   Родительский компонент по ресурсу
        self.res_parent_component = None

        #   Пространство имен объекта
        self.evalSpace = self.GetContext()
        self.evalSpace['self'] = self
        self.evalSpace['evt'] = None
        self.evalSpace['event'] = None

        #   Уникальный идентификатор описания объекта (ресурс)
        self._uuid = component['_uuid']

        if not self._uuid:
            self._bUuidGen = True
            self._uuid = ic_uuid.get_uuid()
        else:
            #   Признак того, что uuid компонента сгенерирован в конструкторе
            self._bUuidGen = False

        if not bGenUUID:
            self._uuidObject = self._uuid

        #   Атрибут задает выражение, которое выполняется после создания обоъекта
        self.init_expr = component['init_expr']

        #   Версии спецификации
        self.__version__base = component['__version__base']
        self.__version__ = component['__version__']

        # Инициализируем модуль ресурса
        #   Модуль обработчиков объекта
        self.__obj_module = None
        #   Модуль обработчиков ресурса
        self.__file_res_mod = None
        #   Инициализируем модуль ресурса
        self.init_res_module()
        #   Инициализируем модуль объекта
        self.init_obj_module()

        # Буфер данных
        self._data_buff = None
        # Ссылка на объект управления объектом
        self._manager = None
        self._manager_class = None
        self.init_manager()

    def getDescription(self):
        return self.description

    def getName(self):
        return self.name

    def init_manager(self):
        """
        Инициализация менеджера управления объектом.
        """
        res_module = self.get_res_module()
        if res_module:
            self._manager_class = getattr(res_module, 'manager_class', None)
            # Создаем контролер
            if self._manager_class:
                if self.GetContext().get('__manager_object', None):
                    self._manager = self.GetContext()['__manager_object']
                else:
                    self._manager = self._manager_class()
                    self._manager.set_object(self)
                    self._manager.Init()
                    self.GetContext()['__manager_object'] = self._manager
            else:
                io_prnt.outWarning(u'Не определен класс менеджера компонента <%s> модуль: <%s>' % (self.__class__.__name__,
                                                                                                   res_module))

    def get_manager(self):
        """
        Возвращает объект управления компонентом.
        """
        return self._manager

    # Другое название функции
    GetManager = get_manager

    def get_manager_class(self):
        return self._manager_class

    def set_resource_property(self):
        lst_keys = [x for x in self.resource.keys() if not x.startswith('__')]
        for key in lst_keys:
            setattr(self, key, self.resource[key])

    def init_res_module(self):
        """
        Инициализируем модули обработчиков (объекта/ресурса).
        """
        res = self.resource
        #   Прописываем модуль ресурса
        if self.GetContext().get('res_module', None):
            self.__file_res_mod = self.GetContext()['res_module']

        #   Грузим модуль ресурса, если он определен в атрибуте 'res_module'
        if res.get('res_module', None) and self.GetContext().get('__file_res', None):
            fn = os.path.dirname(self.GetContext()['__file_res'])+'/'+res['res_module']

            if not os.path.isfile(fn):
                return io_prnt.outWarning(u'\t(!) Resource module: <%s> is not found' % fn)

            try:
                mod = None
                # Проверяем загружен ли модуль с таким имененм или нет
                if self.GetContext().get('res_module', None):
                    if self.GetContext()['res_module'].__file__.replace('.pyc', '.py') == fn:
                        mod = self.GetContext()['res_module']

                # Загружаем модуль, если не загружен
                if not mod:
                    mod = util.icLoadSource(res['res_module'].replace('.', '_'), fn)
                    io_prnt.outLog(u'\t(+) Load resource module: <%s>' % fn)

                if not self.GetContext().get('res_module', False):
                    self.GetContext()['res_module'] = mod
                    self.__file_res_mod = mod
            except:
                io_prnt.outErr(u'\t(-) Not load resource module: <%s>' % fn)

    def init_obj_module(self):
        """
        Инициализация модуля объекта. depricated.
        """
        if self.resource.get('obj_module', None):
            fn = os.path.dirname(self.GetContext()['__file_res'])+'/'+self.resource['obj_module']
            try:
                mod = util.icLoadSource(self.resource['obj_module'].replace('.', '_'), fn)
                self.__obj_module = mod
            except:
                io_prnt.outErr(_('\t(-) Failed to import object module: [%s : %s]') % (self.resource['obj_module'], fn))

    def get_children_lst(self):
        """
        Возвращает список дочерних компонентов.
        """
        return self.component_lst

    def get_children_dct(self):
        """
        Возвращает словарь дочерних компонентов.
        """
        return self.components

    def reg_child(self, obj, name=None):
        """
        Регестрируем дочерний компонентов.
        """
        self.component_lst.append(obj)
        if name:
            self.components[name] = obj
        else:
            self.components[obj.name] = obj

        obj.res_parent_component = self

    def get_res_module(self):
        """
        Возвращает модуль ресурса.
        """
        return self.__file_res_mod

    def get_obj_module(self):
        """
        Возвращает модуль ресурса.
        """
        return self.__obj_module

    def GetComponentsList(self):
        """
        Возвращает список дочерних компонентов по ресурсу.
        """
        if self.evalSpace and self.resource:
            for attr in icDefInf.icContainerAttr:
                if attr in self.resource and isinstance(self.resource[attr], list):
                    lst = range(len(self.resource[attr]))
                    for indx, res in enumerate(self.resource[attr]):
                        if 'alias' in res and not res['alias'] in [None, '', 'None']:
                            name = res['alias']
                        else:
                            name = res['name']

                        try:
                            lst[indx] = self.components[name]
                        except KeyError:
                            lst[indx] = self.evalSpace['_dict_obj'][name]

                    return lst

    def GetChildByName(self, name):
        """
        По имени находит дочерний элемент.
        @type name: C{string}
        @param name: Имя дочернего элемента.
        """
        lst = self.GetComponentsList()
        for el in lst:
            if el.name == name:
                return el

    def FindObjectByName(self, name):
        """
        Найти каскадно объект среди всех дочерних по имени.
        @type name: C{string}
        @param name: Имя дочернего элемента.
        """
        children = []
        if self.IsSizer():
            children = self.objectList
        else:
            children = self.component_lst

        for obj in children:
            if obj.name == name:
                return obj
            if obj.isChildren():
                find_obj = obj.FindObjectByName(name)
                if find_obj:
                    return find_obj
        # Все таки не нашли
        return None

    def getAllChildrenNames(self):
        """
        Список всех дочерних объектов. Рекурсивно.
        """
        children = list()
        if self.IsSizer():
            children = self.objectList
        else:
            children = self.component_lst

        children_names = [child.name for child in children]

        for child in children:
            if child.isChildren():
                child_names = child.getAllChildrenNames()
                if child_names:
                    children_names += child_names
        return children_names

    def isChildren(self):
        """
        У данного объекта есть дочерние?
        """
        return bool(self.components)

    def GetUUIDAttr(self, *attrs):
        """
        Возвращает уникальный иденификатор атрибута компонента.
        """
        return ic_uuid.get_uuid_attr(self.GetUUID(), *attrs)

    def GetPropertyKey(self, prop):
        """
        Функция возвращает ключ, которые генерируется по имени свойства и
        ресурсному описанию компонента.
        """
        if self.GetUUID() and not self._bUuidGen:
            key = self.GetUUIDAttr(prop)
        elif ('_root_obj' in self.evalSpace and self.evalSpace['_root_obj'] and
              self.evalSpace['_root_obj'] != self):
            key = self.evalSpace['_root_obj'].name+self.type+self.name+':'+prop
        else:
            key = self.type+self.name+':'+prop
        return key

    def GetResource(self):
        """
        Возвращает ресурсное описание.
        """
        return self.resource

    def GetRunTimeMode(self):
        """
        Возвращает режим работы компонента.
        """
        if '__runtime_mode' in self.evalSpace:
            return self.evalSpace['__runtime_mode']
        else:
            return 0

    def SaveUserProperty(self, prop, value):
        """
        По возможности сохраняет свойство в настройках пользователя.
        @type prop: C{string}
        @param prop: Имя свойства.
        @type value: C{...}
        @param value: Значение свойства.
        @rtype: C{bool}
        @return: Признак успешного сохранения.
        """
        if self.saveChangeProperty:
            key = self.GetPropertyKey(prop)
            try:
                #   Проверяем на допустимые значение сохраняемых атрибутов. А то бывали
                #   случаи, когда сохранялись отрицательные значения и форма при создании
                #   становится не доступной для польозователя.
                if prop in ('position', 'size'):
                    if value[0] >= -1 and value[1] >= -1:
                        resource.icSetUserVariable(key, value)
                else:
                    resource.icSetUserVariable(key, value)
            except:
                pass

    def LoadUserProperty(self, prop):
        """
        Читает значение определенного свойства из настроек пользователя.
        @type prop: C{string}
        @param prop: Имя свойства.
        @return: Значение сохраненного ранее свойства.
        """
        value = None
        if self.saveChangeProperty:
            try:
                key = self.GetPropertyKey(prop)
                value = resource.icGetUserVariable(key)
                if prop in ('position', 'size') and value:
                    x, y = value
                    if x < -1 or y < -1:
                        msg.MsgBox(None, _('Invalid attribute value: <%s>=%s, component: <%s:%s>')
                                   % (prop, str(value), self.type, self.name))
                        value = None
            except:
                io_prnt.outErr(u'<< Unable load user property %s>>' % prop)

        return value

    def _prepare_expression(self, expr):
        """
        Подготовка выражения для выполнения.
        В случае если в выражении присутствуют символы перевода каретки,
        то при выполнении появляется исключение
        SyntaxError: unexpected character after line continuation character.
        Чтобы этого не происходило удаляются все символы новой строки/перевода каретки
        из исполняемого выражения.
        @param expr: Само выражение. Если не строка, то остается без изменений.
        @return: Подготовленное выражение.
        """
        if type(expr) in (str, unicode):
            expr = expr.strip()
            if expr.startswith('@'):
                expr = expr.replace('\\n', '\n').replace('\\r', '\r')
        return expr

    def getExpression(self, attr):
        """
        Получить выражение для последующего выполнения.
        @type attr: C{string}
        @param attr: Имя атрибута.
        @return: Подготовленное выражение.
        """
        expr = self.resource[attr]
        return self._prepare_expression(expr)

    def eval_attr(self, attr, subkey='', bReUse=True):
        """
        Функция вычисления атрибутов.
        @type attr: C{string}
        @param attr: Имя атрибута.
        @type subkey: C{string}
        @param subkey: Имя уточняющего ключа.
        @type bReUse: C{bool}
        @param bReUse: Признак посторного использования компилированного выражения.
        @return: Код ошибки из модуля coderror, Возвращаемое значение вычисляемого выржения.
        """
        expr = self.getExpression(attr)
        if self.GetUUID() and bReUse:
            compileKey = self.GetUUIDAttr(attr, subkey)
        else:
            compileKey = None

        self.evalSpace['self'] = self
        msg = msgEvalAttrError % (self.name, attr, compileKey)
        return util.ic_eval(expr, self.logType, self.evalSpace, msg, None, compileKey)

    def eval_event(self, attr, evt=None, bSkip=False):
        """
        Обработчик события.
        """
        if self.context['__runtime_mode'] != util.IC_RUNTIME_MODE_EDITOR:
            self.context['event'] = self.context['evt'] = evt
            self.eval_attr(attr)

        if bSkip and evt:
            evt.Skip()

    def eval_expr(self, expr, subkey='expr', bReUse=True ):
        """
        Функция вычисления атрибутов.
        @type expr: C{string}
        @param expr: Вычисляемое выражение.
        @type subkey: C{string}
        @param subkey: Имя уточняющего ключа.
        @type bReUse: C{bool}
        @param bReUse: Признак повторного использования компилированного выражения.
        @return: Код ошибки из модуля coderror, Возвращаемое значение вычисляемого выржения.
        """
        expr = self._prepare_expression(expr)
        if self.GetUUID() and bReUse:
            compileKey = self.GetUUIDAttr(subkey)
        else:
            compileKey = None

        self.evalSpace['self'] = self
        msg = msgEvalAttrError % (self.name, subkey, compileKey)
        return util.ic_eval(expr, self.logType, self.evalSpace, msg, None, compileKey)

    def countAttr(self, attr, subkey=''):
        """
        Функция возвращает вычисленный атрибут. Если вычислить не удается, то
        возвращается None.
        @return: Возвращает значение атрибута. None - если произошла ошибка при
            вычислении атрибута.
        """
        attr_val = self.getExpression(attr)

        if type(attr_val) not in (str, unicode):
            return None

        if not attr_val:
            return ''

        if self.GetUUID():
            compileKey = self.GetUUIDAttr(attr, subkey)
        else:
            compileKey = None

        self.evalSpace['self'] = self
        msg = 'ERROR in countAttr() type=<%s>, name=<%s>, attr=%s' % (self.type, self.name, attr)
        ret, val = util.ic_eval(attr_val, 0, self.evalSpace, msg, None, compileKey)

        if ret:
            return val
        else:
            return None

    def isICAttrValue(self, attr):
        """
        Функция проверяет заполненность атрибута.
        @type attr: C{string}
        @param attr: Имя атрибута.
        @return: Если атрибут заполненный, то возвращает True,
            иначе False.
        """
        attr_val = self.resource[attr]
        if type(attr_val) in (str, unicode):
            return attr_val.strip() not in ('None', '')
        else:
            return attr_val is not None

    def getDataName(self):
        """
        Наименование данных из контекста/источника данных.
        @return: Наименование данных из контекста/источника данных.
        """
        return self.getICAttr('data_name')

    def getICAttr(self, attr, bExpectedExpr=False, subkey='', bReUse=True):
        """
        Функция вычисляет значение атрибута. Если атрибут вычисляемый,
        то она вычисляет его. Вычисляемый атрибут определяется по счиволу '@'.
        @type attr: C{string}
        @param attr: Имя атрибута.
        @type bExpectedExpr: C{bool}
        @param bExpectedExpr: Признак того, что ожидается, что атрибут является
            вычисляемым. Если True, то проверка на '@' не производится.
        @type bReUse: C{bool}
        @param bReUse: Признак повторного использования компилированного выражения.
        @return: Если атрибут вычисляемый, возвращает вычисленное значение атрибута.
            None - если произошла ошибка при вычислении атрибута. Если атрибут
            не вычисляемый, то возвращется значение атрибута.
        """
        attr_val = self.getExpression(attr)

        if type(attr_val) not in (str, unicode) or not attr_val:
            return attr_val

        if attr_val[0] == '@' or bExpectedExpr:
            if self.GetUUID() and bReUse:
                compileKey = self.GetUUIDAttr(attr, subkey)
            else:
                compileKey = None

            self.evalSpace['self'] = self
            msg = u'ERROR in getICAttr() type=<%s>, name=<%s>, attr=%s' % (self.type, self.name, attr)
            ret, val = util.ic_eval(attr_val, 0, self.evalSpace, msg, None, compileKey)
            if ret:
                return val
            elif attr_val[0] == '@':
                return None

        return attr_val

    def setValue(self, Data_):
        """
        Установить данные в виджет.
        """
        io_prnt.outWarning(u'Не определен метод setValue компонента <%s>' % self.__class__.__name__)

    def getValue(self):
        """
        Получить данные из виджета.
        """
        io_prnt.outWarning(u'Не определен метод getValue компонента <%s>' % self.__class__.__name__)

    def setValueBuff(self, Data_):
        """
        Установить данные в виджет.
        """
        self._data_buff = Data_

    def getValueBuff(self):
        """
        Получить данные из виджета.
        """
        return self._data_buff

    def getDataObjectsDct(self):
        """
        Возвращает объекты, у которых заполненно поле data_name в ресурсе.
        """
        dct = {}
        for obj in self.context.GetObjectLst():
            key = obj.resource.get('data_name', None)
            
            # Может быть определены несколько полей данных для контрола
            if key is None:
                key = obj.resource.get('data_names', None)
                
            if key:
                dct[key] = obj
        return dct

    def getChildrenData(self):
        """
        Получить значения дочерних элементов в виде словаря.
        Данные организуются по принципу:
        {
         'Значение data_name элемента': результат функции getValue() элемента.
         ...
        }
        @return: Возвращает заполненный словарь данных.
        """
        data = {}

        if self.IsSizer():
            children = self.objectList
        else:
            children = self.component_lst
        
        for child in children:
            try:
                data_name = child.resource.get('data_name', None)
                data_names = child.resource.get('data_names', None)
                if hasattr(child, 'getValue') and data_name:
                    data[data_name] = child.getValue()
                if hasattr(child, 'getValue') and data_names:
                    values = child.getValue()
                    for i, data_name in enumerate(data_names):
                        data[data_names] = values[i]
                        
                # Обработать дочерние элементы
                if child.isChildren():
                    child_data = child.getChildrenData()
                    if child_data:
                        data.update(child_data)
            except wx.PyDeadObjectError:
                io_prnt.outErr(u'Ошибка определения дочернего элемента')
        return data
    
    def setChildrenData(self, Data_):
        """
        Установить значения дочерних элементов.
        Значения представлены в виде словаря:
        {
         'Значение data_name элемента': результат функции getValue() элемента.
         ...
        }
        """
        if not Data_:
            return False
        
        if self.IsSizer():
            children = self.objectList
        else:
            children = self.component_lst
        
        for child in children:
            try:
                data_name = child.resource.get('data_name', None)
                data_names = child.resource.get('data_names', None)
                if hasattr(child, 'setValue') and data_name and data_name in Data_:
                    child.setValue(Data_[data_name])
                if hasattr(child, 'setValue') and data_names:
                    values = []
                    for i, data_name in enumerate(data_names):
                        value = Data_.get(data_name, None)
                        values.append(value)
                    child.setValue(values)
                # Обработать дочерние элементы
                if child.isChildren():
                    child.setChildrenData(Data_)
            except wx.PyDeadObjectError:
                io_prnt.outErr(u'Ошибка определения дочернего элемента')
                
        return True
        
    def find_child_resource(self, child_name, res=None):
        """
        Поиск ресурса дочернего объекта рекурсивно по имени.
        @param child_name: Имя дочернего объекта.
        @param res: Ресурс. Если не определен, то берется self.resource.
        @return: Словарь ресурса найденного объекта или None
            если не найдено.
        """
        if res is None:
            res = self.GetResource()

        return resource.find_child_resource(child_name, res)

    def IsSizer(self):
        """
        Возвращает признак сайзера.
        """
        return False


class icBase(icSimple, icShape):
    """
    Базовый класс для базовыз визуальных компонентов библиотеки ic.
    """

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bPrepareProp=False):
        """
        Конструктор для создания icBase.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """
        component = util.icSpcDefStruct(SPC_IC_BASE, component)
        icSimple.__init__(self, parent, id, component, logType, evalSpace, bPrepareProp=bPrepareProp)
        icShape.__init__(self, parent, id, component, logType, evalSpace)

        #   Признак принадлежности к видимой области формы. Признак необходим
        #   для контейнеров
        self.bStatusVisible = True

        #   Атрибуты при добавлении в сайзер
        self.size = component['size']
        self.position = component['position']
        self.span = component['span']
        self.proportion = int(component['proportion'])
        self.flag = component['flag']
        self.border = component['border']

        #   Флаг, указывающий, что необходимо сохранять изменяющиеся
        #   параметры окна.
        self.saveChangeProperty = False

    def IsSizer(self):
        """
        Возвращает признак сайзера.
        """
        return False

    def SetStatusVisible(self, bVisible=True, lst=None):
        """
        Функция устанавливает признак, по которому программа определяет
        нужно ли данному компоненту обновлять представление при изменении данных.
        Например, для всех объектов неактивный страницы органайзера этот признак
        будет устанавливаться в False. Для компонента 'icNotebook' эта функция
        переопределена т. к. только на активной странице компоненты видимы.
        @type bVisible: C{bool}
        @param bVisible: Признак обновления представления объекта данных.
        @type lst: C{list}
        @param lst: Список видимых объектов.
        @rtype: C{list}
        @return: Список видимых объектов.
        """
        self.bStatusVisible = bVisible
        if lst is None:
            lst = []
        if bVisible:
            lst.append(self.name)
        try:
            #   Устанавливаем у дочерних объектов такой же признак видимости
            for child in self.components:
                try:
                    self.components[child].SetStatusVisible(bVisible, lst)
                except:
                    pass
        except:
            pass
        return lst


class icSizer(icBase):
    """
    Базовый класс для всех сайзеров.
    """

    DESIGN_SHAPE_COLOR = (230, 240, 255)

    def __init__(self, parent, id=-1, component={}, logType=0, evalSpace=None,
                 sizer=None, bPrepareProp=False):
        """
        Конструктор базового класса сайзеров.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type sizer: C{icSizer}
        @param sizer: Ссылка на родительский сайзер.
        """
        util.icSpcDefStruct(SPC_IC_SIZER, component)
        icBase.__init__(self, parent, id, component, logType, evalSpace, bPrepareProp=bPrepareProp)

        #   Список содержащихся компонентов
        self.objectList = []
        self.itemList = []
        self.cursorBorder = 1
        self.contaningSizer = None
        # Ссылка на родительский сайзер.
        self.parent_sizer = sizer
        self.__name = self.name

    def GetName(self):
        return self.__name

    def SetName(self, name):
        self.__name = name

    def GetRect(self):
        """
        Возвращает прямоугольную область расположения сайзера.
        """
        try:
            x, y = self.GetPosition()
        except:
            x, y = self.position

        try:
            sx, sy = self.GetSize()
        except:
            sx, sy = self.size

        return wx.Rect(x, y, sx, sy)

    def GetParent(self):
        """
        Возвращает ссылку на родительский объект - для сайзера в библиотеке
        ic возвращается ссылка на компонент, на котором размещается сайзер.
        """
        # log.debug(u'Получение родительского объекта сайзера <%s>' % self.__name)
        return self.parent

    def regObject(self, obj):
        """
        Зарегистрировать объект во внутренних списках виджета.
        @param obj: Объект.
        """
        self.objectList.append(obj)

    def Add(self, obj, proportion=0, flag=0, border=0):
        """
        Функция добавления в сайзер. Она переопределена для того, чтобы
        контролировать комопненты, которые добавляются, т. к. стандартные
        сайзеры этого делать не позволяют.

        ВНИМАНИЕ! Проблемная функция. Ее использование может вызывать
        исключение <Segmentation fault>. В этом случае рекомендуется использовать
        стандартные функции Add сайзера.
        """
        item = wx.SizerItem()
        item.SetProportion(proportion)
        item.SetFlag(flag)
        try:
            item.SetBorder(border)
        except:
            io_prnt.outLog('SetBorder Failed in obj: <%s>' % obj)

        bCreate = True
        bSpacer = False
        try:
            if obj.type == 'SizerSpace':
                item.SetSpacer(obj.GetSize())
            elif 'IsSizer' in dir(obj) and obj.IsSizer():
                item.AssignSizer(obj)
            else:
                item.SetWindow(obj)
                if 'size' in dir(obj):
                    self.SetItemMinSize(obj, obj.size)
        except:
            bCreate = False
            io_prnt.outLastErr('Error in Sizer.Add()')

        if bCreate:
            self.AddItem(item)
            self.itemList.append(item)
            self.regObject(obj)
            obj.contaningSizer = self

        return bCreate

    def getChildrenItems(self):
        return self.itemList
    
    def removeItem(self, item):
        """
        Функция удаления из сайзера. Она переопределена для того, чтобы
        контролировать комопненты, которые добавляются, т. к. стандартные
        сайзеры этого делать не позволяют.
        """
        if item:
            obj = item.GetWindow()
            if obj:
                if obj in self.objectList:
                    obj_idx = self.objectList.index(obj)
                    del self.objectList[obj_idx]
                # ВНИМАНИЕ! Т.к. сайзеры являются наследниками icSimple
                # тогда регистрация объектов производится
                # также в component_lst и components
                if obj in self.component_lst:
                    obj_idx = self.component_lst.index(obj)
                    del self.component_lst[obj_idx]
                self.components = dict([(name, component) for name, component in self.components.items() if component != obj])

                self.Remove(obj)
                obj = None
            if item in self.itemList:
                item_idx = self.itemList.index(item)
                del self.itemList[item_idx]            
            return True
        return False
        
    def GetIndex(self, obj):
        """
        Возвращает индекс объекта в списке объектов сайзера.
        @type obj: C{...}
        @param obj: Ссылка на объет, индекс которого ищется.
        """
        for indx, x in enumerate(self.objectList):
            try:
                if x == obj:
                    return indx
            except:
                io_prnt.outErr('GetIndex ERROR')

        return -1

    def Reconstruct(self):
        pass

    def DrawShape(self, dc=None):
        """
        Рисует представление сайзера для графического редактора форм.
        """
        pass

    def SetFocus(self):
        """
        Установка фокуса.
        """
        pass

    def IsSizer(self):
        """
        Возвращает признак сайзера.
        """
        return True


class icEvent:
    """
    Обкладка на обработчик событий. Временная заглушка для перехода с
    wxPython 2.4.2.1 на wxPython 2.5.1.
    """
    def __init__(self):
        pass


class icWidget(icBase, icEvent):
    """
    Базовый класс для визуальных компонентов, работающий с объектами
    данных.
    """

    def __init__(self, parent, id=-1, component=None, logType=0,
                 evalSpace=None, bPrepareProp=False):
        """
        Конструктор для создания icWidget.
        @type parent: C{wx.Window}
        @param parent: Указатель на родительское окно
        @type id: C{int}
        @param id: Идентификатор окна
        @type component: C{dictionary}
        @param component: Словарь описания компонента
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога)
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений
        @type evalSpace: C{dictionary}
        """
        #   Дополняем описание до спецификации
        component = util.icSpcDefStruct(SPC_IC_WIDGET, component)
        icBase.__init__(self, parent, id, component, logType, evalSpace, bPrepareProp=bPrepareProp)
        icEvent.__init__(self)

        #   Имя объекта данных
        self.source = component['source']
        #   Объект данных
        self.dataset = util.getICDataObj(self.source, evalSpace)
        #   Указатель на интерфейс к классу данных
        if self.dataset:
            self.idataclass = self.dataset.GetIDataclass()
        else:
            self.idataclass = None
        #   Атрибут определяет список обновляемых компонентов
        self.refresh = component['refresh']
        #   Атрибут определяет список песчитываемых компонентов
        self.recount = component['recount']
        #   Атрибут определяет показывать компонент или нет
        self.bShow = component['show']
        #   Атрибут определяет выражение, выполняемое после нажатия любой кнопки в компоненте.
        self.keydown = component['keyDown']
        #   Атрибут определяет имя компонента в очереди переходов по TAB, после
        #   которого текущий компонент должен быть помещен.
        self.moveAfterInTabOrder = component['moveAfterInTabOrder']
        #   Версии спецификации
        self.__version__icwidget = component['__version__icwidget']
        #   Выражение обработки сообщения <icEvents.EVT_POST_INIT>
        self.onInit = component['onInit']
        #   Флаг блокировки перерисавывания компонента, используется
        #   если опрделен обработчик на событие <EVT_PAINT>
        self._blockEvtPoint = False

        self.enable = component['enable']
        if not self.enable:
            wx.CallAfter(self.Enable, False)

    def isEnabled(self):
        """
        Объект включен?
        @return: True/False.
        """
        if hasattr(self, 'IsEnabled'):
            return self.IsEnabled()
        return self.enable

    def DirectRefresh(self):
        """
        Посылает сообщение на перерисовку компонента.
        """
        evt = wx.PaintEvent(self.GetId())
        return self.GetEventHandler().ProcessEvent(evt)

    def GetBestSize(self):
        return wx.Size(*self.GetResource()['size'])

    def GetDataset(self):
        """
        Возвращает указатель на объект индексированного доступа к классу
        данных.
        """
        return self.dataset

    def GetIDataclass(self):
        """
        Возвращает указатель на интерфейс работы с классом данных.
        """
        if self.dataset:
            return self.dataset.GetIDataclass()

    def BindICEvt(self):
        """
        Регестрирует события, используемые системой визуализации.
        Вызываются только после конструкторов базовых классов.
        """
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_DOWN, self.BackPropKeyDownEvt)

        if self.onInit:
            self.Bind(icEvents.EVT_POST_INIT, self.OnInit)

        # Создаем wx обработчики для сигнальной системы
        try:
            for con in self.srcCntLst:
                if con.src and issubclass(con.src.__class__, icsignalsrc.icWxEvtSignalSrc):
                    self.Bind(con.src.evt_id, self._generate_signal)
        except:
            io_prnt.outErr(_('ERROR: Init source signal error.'))

    def _generate_signal(self, evt):
        """
        Генерирует сигналы.
        """
        # Определяем соединение
        for con in self.srcCntLst:
            if evt.GetEventType() == con.src.get_signal_type():
                sign = con.src.generate(evt, self)
                if con.src.isWxSkip():
                    evt.Skip()
                self.send_signal(sign, con)

    def BlockKeyDownEvent(self):
        """
        Блокирует сообщения от клавиатуры.
        """
        self.evalSpace['__block_key_down'] = True

    def UnBlockKeyDownEvent(self):
        """
        Разблокирует сообщения от клавиатуры.
        """
        self.evalSpace['__block_key_down'] = False

    def OnKeyDown(self, evt):
        """
        Стандартный обработчик события <EVT_KEY_DOWN> -атрибут 'keyDown'.
        """
        if self.evalSpace['__block_key_down']:
            return
        bSkip = True
        if self.keydown:
            self.evalSpace['self'] = self
            self.evalSpace['evt'] = evt
            self.evalSpace['event'] = evt
            ret, val = self.eval_attr('keyDown')
            if ret and not val is None:
                try:
                    bSkip = bool(val)
                except:
                    log.fatal()
                    bSkip = True
        if bSkip:
            evt.Skip()

    def OnInit(self, evt):
        """
        Обрабатываем сообщение <icEvents.EVT_POST_INIT>.
        """
        self.evalSpace['evt'] = evt
        self.evalSpace['event'] = evt
        if 'onInit' in self.resource:
            self.eval_attr('onInit')
        else:
            io_prnt.outLog('### KeyError obj=(%s, %s, %s)'
                           % (self.resource['name'], self.resource['type'], self))
        evt.Skip()

    def PostOnInitEvent(self):
        """
        Посылает сообщение <icEvents.EVT_POST_INIT>.
        """
        event = icEvents.icPostInitEvent(icEvents.icEVT_POST_INIT, self.GetId())
        return self.GetEventHandler().AddPendingEvent(event)

    def UpdateRelObj(self, lstUpdate = None):
        """
        Изменяет состояния компонентов, работающих с источниками данных.
        @type lstUpdate: C{list}
        @param lstUpdate: Список объектов, которые необходимо обновить.
        """
        if self.dataset is None:
            _classname = None
        else:
            _classname = self.dataset.name
        #   Если список объектов для обновления не задан, то в качестве списка берем
        #   список, определенный в атрибуте 'refresh' описания компонента
        if lstUpdate is None:
            try:
                lstUpdate = self.refresh
            except:
                pass
        #   Определяем алиас объекта
        try:
            alias = self.resource['alias']
        except:
            alias = None
        #   Если список объектов для обновления не задан, то обновляются только объекты
        #   имеющие в описании атрибут 'source'.
        if lstUpdate in [None, '', 'None']:
            for key in self.evalSpace['_has_source'].keys():
                try:
                    if key not in [self.name, alias]:
                        self.evalSpace['_has_source'][key].UpdateViewFromDB(_classname)
                except:
                    pass

        #   Если список объектов задан, то обновляем только эти объекты
        else:
            for key in lstUpdate:
                try:
                    if key not in [self.name, alias]:
                        self.evalSpace['_dict_obj'][key].UpdateViewFromDB(_classname)
                except:
                    pass

    def UpdateRelObjDB(self, lstUpdate = None):
        """
        Изменяет данные в классах данных.
        @type lstUpdate: C{list}
        @param lstUpdate: Список объектов, которые необходимо обновить
        """
        if self.dataset is None:
            _classname = None
        else:
            _classname = self.dataset.name
        #   Если список объектов для обновления не задан, то в качестве списка берем
        #   список, определенный в атрибуте 'refresh' описания компонента
        if lstUpdate is None:
            try:
                lstUpdate = self.refresh
            except:
                pass
        #   Определяем алиас объекта
        try:
            alias = self.resource['alias']
        except:
            alias = None

        #   Если список объектов для обновления не задан, то обновляются только объекты
        #   имеющие в описании атрибут 'source'.
        if lstUpdate is None:
            for key in self.evalSpace['_has_source'].keys():
                try:
                    if key not in [self.name, alias]:
                        self.evalSpace['_has_source'][key].UpdateDataDB(_classname)
                except:
                    pass
        #   Если список объектов задан, то обновляем только эти объекты
        else:
            for key in lstUpdate:
                try:
                    if key not in [self.name, alias]:
                        self.evalSpace['_dict_obj'][key].UpdateDataDB(_classname)
                except:
                    pass

    def BackPropKeyDownEvt(self, evt):
        """
        Посылает сообщение главному окну формы, о нажатии клавиши.
        """
        if self.evalSpace['__block_key_down']:
            return
        #   Ищем родителя
        if self.evalSpace.get('_root_obj', None) != self:
            prnt = self.GetParent()
            src = None
            while prnt:
                attrs = dir(prnt)
                if 'keydown' in attrs and prnt.keydown:
                    src = prnt
                    break
                elif self.evalSpace.get('_root_obj', None) == prnt:
                    break
                else:
                    prnt = prnt.GetParent()
            if src:
                try:
                    event = evt.Clone()
                    src.GetEventHandler().AddPendingEvent(event)
                except:
                    io_prnt.outErr('BackPropKeyDownEvt Error')
        evt.Skip()

    def getRootObject(self):
        """
        Определить самый корневой объект.
        """
        parent = self.GetParent()
        if parent:
            try:
                return parent.getRootObject()
            except:
                io_prnt.outErr(u'Ошибка определения корневого элемента объекта <%s>' % self.name)
                return None
        else:
            return self


class icShortHelpString(wx.PopupWindow):
    """
    Класс реализации всплывающей подсказки.
    """

    def __init__(self, parent, text, pos=(0, 0), time=1000):
        """
        Конструктор всплывающей подсказки.
        @type parent: C{wx.Window}
        @param parent: Родительское окно.
        @type text: C{string}
        @param text: Текст подсказки.
        @type pos: C{wx.Point}
        @type pos: Позиция подсказки.
        @type time: C{float}
        @param time: Период времени (в милисекундах) после которого подсказка уничтожается.
        """
        wx.PopupWindow.__init__(self, parent, 0)
        self.SetBackgroundColour(wx.Colour(255, 255, 206))
        # Сделать поправку для Linux
        if wx.Platform == '__WXGTK__':
            if parent:
                parent_screen_pos = parent.GetScreenPosition()
                pos = wx.Point(pos[0]+parent_screen_pos.x, pos[1]+parent_screen_pos.y)
        self.SetPosition(pos)

        self.font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, encoding=wx.FONTENCODING_CP1251)
        self.text = text = text.replace('\\r\\n', '\r\n').replace('\r\n', '\n')
        sz = self.GetBestSizeRect()
        self.SetSize((sz.width+4, sz.height+2))
        self.edgeClr = (155, 155, 148)
        self.timer = None
        self.bNextPeriod = False
        self.SetDestroyTimer(time)
        self.Show(True)
        old_win = getHelpStringWin()
        if old_win:
            try:
                old_win.Show(False)
                old_win.Destroy()
            except:
                pass

        setHelpStringWin(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def GetBestSizeRect(self):
        lineLst = self.text.split('\n')
        w, h = self.GetTextExtent('W')
        sx, sy = 0, 0
        sy = len(lineLst) * h
        for r in lineLst:
            w, h = self.GetTextExtent(r)
            if sx < w:
                sx = w
        return wx.Size(sx+4, sy+4)

    def Draw(self, dc):
        """
        Отрисовка.
        """
        dc.BeginDrawing()
        bgr, fgr = self.GetBackgroundColour(), self.GetForegroundColour()
        backBrush = wx.Brush(bgr, wx.SOLID)
        pen = wx.Pen(wx.Colour(*self.edgeClr))
        dc.SetBackground(backBrush)
        dc.SetPen(pen)
        dc.SetBrush(backBrush)
        dc.SetFont(self.font)
        width, height = self.GetClientSize()
        dc.DrawRectangle(0, 0, width, height)
        pen = wx.Pen(fgr)
        dc.SetPen(pen)
        labelLine = self.text.split('\n')
        w, h = self.GetTextExtent('W')
        y = (height - h*len(labelLine))/2
        for line in labelLine:
            if line == '':
                w, h = self.GetTextExtent('W')  # empty lines have height too
            else:
                w, h = self.GetTextExtent(line)

            x = 5
            dc.DrawText(line, x, y)
            y += h
        bgr_prnt = self.GetParent().GetBackgroundColour()
        graphicUtils.drawRoundCorners(dc, (width, height),
                                      fgr, bgr,
                                      bgr_prnt, 0,
                                      (self.edgeClr, self.edgeClr, self.edgeClr, self.edgeClr))
        dc.EndDrawing()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def SetDestroyTimer(self, tm):
        """
        Устанавливает таймер на уничтожение.
        """
        # We're going to use a timer to drive a 'clock' in the last
        # field.
        if tm > 0:
            self.timer = wx.PyTimer(self.Notify)
            self.timer.Start(tm)
            self.bNextPeriod = False

    def Notify(self):
        """
        Handles events from the timer we started in __init__().
        We're using it to drive a 'clock' in field 2 (the third field).
        """
        try:
            if not self.bNextPeriod:
                self.Show(False)
                self.Destroy()
            else:
                self.bNextPeriod = False
        except:
            pass
