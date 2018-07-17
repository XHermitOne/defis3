#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Создает диалоговое окно.
Содержит описание класса icDialog, который по ресурсному описанию создает диалоговое окно.

@type SPC_IC_DIALOG: C{dictionary}
@var SPC_IC_DIALOG: Спецификация на ресурсное описание диалогового окна. Описание ключей SPC_IC_DIALOG:

    - B{name = 'default'}: Имя окна.
    - B{type='Dialog'}: Тип объекта.
    - B{title = 'Dialog'}: Заголовок окна.
    - B{position = (-1,-1)}: Расположение окна.
    - B{size = (-1,-1)}: Размер окна.
    - B{foregroundColor=None}: Цвет текста.
    - B{backgroundColor=None}: Цвет фона.
    - B{onClose = None}: Выражение, выполняемое при закрытии окна (обработка события EVT_CLOSE).
        Если выражение вернет False, то окно не будет закрыто (не будет вызываться evt.Skip() ).
    - B{setFocus = None}: Выражение, выполняемое при установлении фокуса на диалог (обработка события EVT_SET_FOCUS).
    - B{killFocus = None}: Выражение, выполняемое при потере фокуса на диалог (обработка события EVT_KILL_FOCUS).
    - B{style=0}: Стиль окна.
    - B{keyDown=None}: Выражение, выполняемое после нажатия любой кнопки в любом компоненте,
        который распологается на диалоговом окне.
    - B{child=[]}: Cписок дочерних элементов.

@type ICDialogStyle: C{dictionary}
@var ICDialogStyle: Словарь специальных стилей компонента. Описание ключей ICDialogStyle:

    - C{wx.CAPTION} - Поле для перетаскивания окна.
    - C{MINIMIZE_BOX} - Выводит кнопку для минимизации.
    - C{MAXIMIZE_BOX} - Выводит кнопку для полного развертывания.
    - C{wx.DEFAULT_DIALOG_STYLE} - Стиль по умолчанию комбинация wxCAPTION и wxSYSTEM_MENU (не используется под Unix).
    - C{wx.RESIZE_BORDER} - Позволяет изменять размеры окна;
    - C{wx.SYSTEM_MENU} - Выводит системное меню;
    - C{wx.THICK_FRAME} - Выдодит тонкий бордюр вокруг окна.
    - C{wx.STAY_ON_TOP} - Диалог остается поверх всех окон (только Windows).
    - C{wx.NO_3D} - Под Windows определяет, что дочерний объект не будет иметь 3D бордюры, если это не будет определено в самом компоненте.
    - C{wx.DIALOG_NO_PARENT} - По умолчанию диалоги создаваемые с parent = NULL будут брать верхнее окно приложения в качестве родительского.
        Используйте этот стиль для того, чтобы сделать окно действительно без родителя (этот стиль не рекомендуется для модальных окон).
    - C{wx.DIALOG_EX_CONTEXTHELP} Под Windows, дает запрос на справку (посылается запрос wxEVT_HELP).
"""

import wx
# from ic.dlg.msgbox import MsgBox
# from ic.log.iclog import *
import ic.utils.util as util
from .icwidget import icWidget, SPC_IC_WIDGET
# import ic.utils.resource as resource
# import icEvents
# from ic.kernel import io_prnt
from ic.log import log
# from ic.PropertyEditor import icDefInf
# import ic.imglib.common as common
import ic.PropertyEditor.icDefInf as icDefInf

_ = wx.GetTranslation

ICDialogStyle = {'CAPTION': wx.CAPTION,
                 'DEFAULT_DIALOG_STYLE': wx.DEFAULT_DIALOG_STYLE,
                 'RESIZE_BORDER': wx.RESIZE_BORDER,
                 'SYSTEM_MENU': wx.SYSTEM_MENU,
                 'THICK_FRAME': wx.THICK_FRAME,
                 'STAY_ON_TOP': wx.STAY_ON_TOP,
                 'DIALOG_NO_PARENT': wx.DIALOG_NO_PARENT,
                 'DIALOG_EX_CONTEXTHELP': wx.DIALOG_EX_CONTEXTHELP,
                 'MINIMIZE_BOX': wx.MINIMIZE_BOX,
                 'MAXIMIZE_BOX': wx.MAXIMIZE_BOX
                 }

SPC_IC_DIALOG = {'name': 'Dialog',
                 'type': 'Dialog',
                 'child': [],

                 'title': 'Dialog',
                 'position': (-1, -1),
                 'size': (100, 100),

                 'foregroundColor': None,
                 'backgroundColor': None,
                 'style': wx.DEFAULT_DIALOG_STYLE,
                 'onClose': None,
                 'setFocus': None,
                 'killFocus': None,
                 'keyDown': None,
                 'fit': False,  # Сделать образмеривание диалогового окна по дочерним?
                 'icon': None,  # Иконка

                 '__events__': {'onClose': ('wx.EVT_CLOSE', 'OnClose', False),
                                'setFocus': ('wx.EVT_SET_FOCUS', 'OnSetFocus', False),
                                'killFocus': ('wx.EVT_KILL_FOCUS', 'OnKillFocus', False),
                                },
                 '__attr_types__': {0: ['name', 'type'],
                                    icDefInf.EDT_CHECK_BOX: ['fit'],
                                    },
                 '__parent__': SPC_IC_WIDGET,
                 '__attr_hlp__': {'fit': u'Сделать образмеривание диалогового окна по дочерним?',
                                  'icon': u'Иконка',
                                  },
                 }

# -------------------------------------------
#   Общий интерфэйс модуля
# -------------------------------------------

#   Тип компонента
ic_class_type = icDefInf._icWindowType

#   Имя пользовательского класса
ic_class_name = 'icDialog'

#   Описание стилей компонента
ic_class_styles = ICDialogStyle

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_DIALOG
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtDialog'
ic_class_pic2 = '@common.imgEdtDialog'

#   Путь до файла документации
ic_class_doc = 'ic/doc/ic.components.icdialog.icDialog-class.html'

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = ['Dialog', 'Frame', 'ToolBarTool', 'Separator', 'GridCell']

#   Версия компонента
__version__ = (1, 0, 0, 11)


class icDialog(icWidget, wx.Dialog):
    """
    Диалоговое окно.
    """

    canClose = True

    @staticmethod
    def GetDesigner():
        """
        Указатель на класс графического редактора компонента.
        """
        from ic.PropertyEditor.designers import icdialogdesigner
        return icdialogdesigner.icDialogDesigner

    @staticmethod
    def TestComponentResource(res, context, parent, *arg, **kwarg):
        import ic.components.icResourceParser as prs
        log.info(u'Тестирование диалогового окна <%s>' % res['name'])
        testObj = prs.CreateForm('Test', formRes=res,
                                 evalSpace=context, parent=parent, bIndicator=False)
        #   Для оконных компонентов надо вызвать метод Show
        try:
            if testObj.context['_root_obj']:
                testObj.context['_root_obj'].SetFocus()
                testObj.context['_root_obj'].ShowModal()
                testObj.context['_root_obj'].Destroy()
        except:
            log.fatal(u'Ошибка тестирования диалогового окна')

    def __init__(self, parent=None, id=-1, component={}, logType=0,
                 evalSpace=None, bCounter=False, progressDlg=None, *arg, **kwarg):
        """
        Конструктор для создания icDialog.
        @type parent: C{wxWindow}
        @param parent: Указатель на родительское окно.
        @type id: C{int}
        @param id: Идентификатор окна.
        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        """
        #   Атрибуты сайзера
        self.sizer = None
        self.bSizerAdd = False
        self.title = None

        util.icSpcDefStruct(SPC_IC_DIALOG, component)
        icWidget.__init__(self, parent, id, component, logType, evalSpace)

        self.title = self.getTitle()
        pos = component['position']
        self.size = component['size']
        fgr = component['foregroundColor']
        bgr = component['backgroundColor']
        self.style = style = component['style'] | wx.WANTS_CHARS
        self.on_close = component['onClose']
        self.set_focus = component['setFocus']
        self.kill_focus = component['killFocus']
        icon = component['icon']

        #   Флаг, указывающий, что необходимо сохранять изменяющиеся
        #   параметры окна (позицию и размеры).
        self.saveChangeProperty = True

        #   Читаем расположение и размеры диалога из файла настроек пользователя
        _pos = self.LoadUserProperty('position')
        _size = self.LoadUserProperty('size')

        if _pos:
            pos = _pos

        if pos[0] > 1000:
            pos[0] = -1
        if pos[1] > 1000:
            pos[1] = -1

        if _size:
            self.size = _size

        # Буфер результата работы с формой
        self.__result_buff = None

        # wx.Dialog.__init__(self, parent, id, self.title, pos, self.size, style = style, name = self.name)
        # Instead of calling wxDialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI dialog using the Create
        # method.

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, id, self.title, pos, self.size, style, self.name)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.this = pre.this

        if icon:
            icon_img = util.ic_eval(icon, evalSpace=self.evalSpace)
            if icon_img:
                icon = wx.IconFromBitmap(icon_img)
                self.SetIcon(icon)

        self.Show(False)
        #   Признак разрушения дочерних элементов
        self._bChildsDestroied = False

        if fgr is not None:
            self.SetForegroundColour(wx.Colour(fgr[0], fgr[1], fgr[2]))

        if bgr is not None:
            self.SetBackgroundColour(wx.Colour(bgr[0], bgr[1], bgr[2]))

        self.SetAutoLayout(True)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.BindICEvt()

        #   Создаем дочерние компоненты
        self.Freeze()
        self.childCreator(bCounter, progressDlg)
        self.Thaw()
        
        if component.get('show', '1') in ('True', 'true', 1):
            self.Show(True)

        if component.get('fit', None):
            self.Fit()

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        if self.child:
            if not self.evalSpace['_root_obj']:
                self.evalSpace['_root_obj'] = self

            self.GetKernel().parse_resource(self, self.child, None, context=self.evalSpace,
                                            bCounter=bCounter, progressDlg=progressDlg)

    def GetResult(self):
        """
        Возвращет результат.
        """
        return self.__result_buff

    def SetResult(self, data):
        """
        Сохраняет значение результата работы формы.
        """
        self.__result_buff = data

    def IsChildDestroied(self):
        """
        Возвращает признак того, что дочерние элементы разрушены.
        """
        return self._bChildsDestroied

    def SetPrzChildDestroied(self, prz=True):
        """
        Устанавливет признак того, что дочерние элементы разрушены.
        """
        self._bChildsDestroied = prz

    def OnSize(self, evt):
        """
        Обрабатывает изменение размеров окна (EVT_SIZE).
        """
        self.Layout()
        self.Refresh()
        evt.Skip()

    def OnSetFocus(self, evt):
        """
        Обрабатывает событие установки фокуса (EVT_SET_FOCUS).
        """
        self.evalSpace['evt'] = evt
        self.eval_attr('setFocus')
        evt.Skip()

    def OnKillFocus(self, evt):
        """
        Обрабатывает событие установки фокуса (EVT_SET_FOCUS).
        """
        self.evalSpace['evt'] = evt
        self.eval_attr('killFocus')
        evt.Skip()

    def ShowModal(self):
        res = wx.Dialog.ShowModal(self)
        if self.get_manager() and hasattr(self.get_manager(), 'is_valid') and res == wx.ID_OK:
            res = self.get_manager().is_valid(dialog=self)
            if res:
                return wx.ID_OK
            else:
                return wx.ID_CANCEL
        return res

    def EndModal(self, ret):
        """
        Завершает диалог.
        @type ret: C{int}
        @param ret: Код возврата.
        """
        self.OnClose(None)
        wx.Dialog.EndModal(self, ret)

    def isPressCancel(self):
        """
        Нажата кнопка <Отмена>?
        """
        return self.GetReturnCode() == wx.ID_CANCEL

    def isPressOk(self):
        """
        Нажата кнопка <OK>?
        """
        return self.GetReturnCode() == wx.ID_OK

    def OnClose(self, evt):
        """
        Обрабатывает сообщение EVT_CLOSE на закрытие окна.
        """
        if not self.canClose:
            log.warning(u'Вкл. запрет на закрытие диалогового окна <%s>' % self.getName())
            return

        if self.isICAttrValue('onClose'):
            self.canClose = False
            self.evalSpace['evt'] = evt
            self.SaveUserProperty('position', self.GetPosition())
            self.SaveUserProperty('size', self.GetSize())
            ret, val = self.eval_attr('onClose')
            #   Если выражение вернет False, то отменяем закрытие окна. None трактуем
            #   как True,  поскольку если выражение не определяет возвращаемое значение,
            #   то ic_eval вернет (True,  None)
            if ret and not val and val not in (None, ''):
                self.canClose = True
            else:
                log.warning(u'Вкл. запрет на закрытие диалогового окна <%s>' % self.getName())
                return

        #   Снимаем блокировки у классов данных
        for key in self.evalSpace['_sources']:
            try:
                self.evalSpace[key].UnlockAll()
            except:
                log.fatal(u'Dialog OnClose Error obj: <%s>' % key)

        self.evalSpace['__block_lock_rec'] = True
        #   Сохраняем буферы
        self.Update(True)
        self.evalSpace['__block_lock_rec'] = False
        self.canClose = True

        if evt:
            evt.Skip()

    def Update(self, bAsk=False):
        """
        Обновление объектов, работающих с данным.
        """
        for obj in self.evalSpace['_has_source'].values():
            try:
                obj.Update(bAsk=bAsk)
                log.debug(u'Update Object: type=<%s>, name=<%s>' % (obj.type, obj.name))
            except:
                log.fatal(u'Ошибка обновления объектов диалоговогоокна, работающих с данными')

    def Destroy(self):
        """
        Разрушение окна.
        """
        #   Запоминаем расположение и размеры диалога в файле настроек пользователя
        self.evalSpace['__block_lock_rec'] = True
        #   Посылаем всем компонентам сообщение, что диалог уничножается
        try:
            for key in self.evalSpace['_dict_obj']:
                try:
                    self.evalSpace['_dict_obj'][key].ObjDestroy()
                except:
                    log.fatal(u'Ошибка разрушения диалогового окна')
        except:
            log.fatal(u'Ошибка разрушения диалогового окна')

        try:
            if self.parent:
                for key in self.parent.components:
                    if self.parent.components[key] == self:
                        self.parent.components.pop(key)
                        break
        except:
            log.fatal(u'DIALOG DESTROY: Warning can\'t pop element in parent.components dictionary.')

        #   Удаляем форму
        wx.Dialog.Destroy(self)

    def getTitle(self):
        """
        Заголовок диалогового окна.
        """
        if self.title is None:
            self.title = self.getICAttr('title') or ''
        return self.title


def test(par=0):
    """
    Тестирет класс icDialog.
    """
    from ic.components.ictestapp import TestApp
    app = TestApp(par)
    dlg = icDialog(None, -1, {'keyDown': 'print(\'KeyDown\')',
                              'setFocus': 'print(\'setFocus\')',
                              'killFocus': 'print(\'killFocus\')',
                              'onClose': 'print(\'onClose\')'})
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    test(0)
