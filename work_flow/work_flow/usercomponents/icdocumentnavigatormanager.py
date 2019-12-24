#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Компонент менеджера навигации документов.

Под навигацией понимаем весь спектр функций/методов, которые можно
выполнять над документом или списком документов.

Функции движения:
first - Переход на первый документ в списке
last - Переход на последний документ в списке
prev - Переход на предыдущий документ в списке
next - Переход на следующий документ в списке
move_to - Перемещение документа по индексу в списке
move_up - Перемещение документа вверх по списку
move_down - Перемещение документа вниз по списку
sort - Сортировка списка документов в заданной последовательности
reverse - Обратная сортировка списка документов в заданной последовательности
find - Поиск документа в списке документов, начиная с текущего
copy - Получить копию текущего документа в Clipboard
paste - Вставить копию документа в список из Clipboard'а
clone - Клонировать документ через Clipboard, но с другим UUID
filter - Применить фильтр к списку документов

Функции оперирования документом:
view - Режим просмотра текущего документа
edit - Режим редактирвания текущего документа
update - Обновление текущего документа
create - Режим создания нового документа
delete - Удаление уже созданного документа
insert - Вставить внешний документ в список по индексу
print - Режим печати текущего документа
print_all - Режим печати всех документов списка
validate - Режим проверки корректности заполнения документа
errors - Просмотр списка ошибок заполнения документа
import - Режим импорта документа из внешнего источника/файла
export - Режим экспорта документа во внешний источник/файл
send - Отправить документа по почте
save - Сохранение текущего документа в БД
save_all - Сохранение всех документов списка в БД
load - Загрузка текущего документа из БД
load_all - Загрузка всех дкументов из БД
show - Отображение текущего документа в альтернативном виде
scheme - Отобразить схему представления для текущего документа
run - Запуск текущего документа на выполнение
stop - Останов выполнения документа
do - Запуск вспомогательных операций документа (аналог проведения)
undo - Отомена вспомогательных операций документа (аналог распроведения)
open - Отрытие текущего документа для действий/операций
close - Загрытие текущего документа для действий/операций
link - Связать с текущим документом другой документ
unlink - Разорвать связь документа с текущим документом
check - Поставить дополнительную метку на текущий документ
uncheck - Снять дополнительную метку c текущего документа
attach - Вложить дополнение в текущий документ
detach - Убрать вложенное дополнение из текущего документа
calc - Произвести дополнительные расчеты связанные с текущим документом
extend - Выполнить дополнительные действия над документом
sum - Выполнить суммирование по реквизиту всех документов списка
count - Подсчет количества документов в списке
upload - Выгрузка документа на сервер
download - Загрузка документа с сервера

Дополнительные функции:
view_requisites - Изменение списка просматриваемых реквизитов в списке докумнтов
etc - Все дополнительные действия над документом или списком документов
settings - Вызов редактора дополнительных настроек документа или списка документов
help - Вызов помощи по документу или списку документов
"""

from ic.components import icwidget

from ic.utils import util
import ic.components.icResourceParser as prs
from ic.bitmap import bmpfunc
from ic.dlg import dlgfunc
from ic.utils import coderror
from ic.log import log
from ic.PropertyEditor import icDefInf
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt

import work_flow.doc_sys.document_navigator_manager as parentModule

#   Тип компонента
ic_class_type = icDefInf._icUserType

#   Имя класса
ic_class_name = 'icDocumentNavigatorManager'

#   Описание стилей компонента
ic_class_styles = {'DEFAULT': 0}

#   Спецификация на ресурсное описание класса
ic_class_spc = {'type': 'DocumentNavigatorManager',
                'name': 'default',
                'child': [],
                'activate': True,
                'init_expr': None,
                '_uuid': None,

                'document': None,
                'list_ctrl': None,
                'columns': None,
                '__styles__': ic_class_styles,
                '__attr_types__': {0: ['name', 'type'],
                                   icDefInf.EDT_TEXTFIELD: ['description'],
                                   icDefInf.EDT_USER_PROPERTY: ['document', 'list_ctrl'],
                                   icDefInf.EDT_PY_SCRIPT: ['columns'],
                                   },
                '__events__': {},
                '__parent__': parentModule.SPC_IC_DOCUMENT_NAVIGATOR_MANAGER,
                '__attr_hlp__': {'document': u'Документ, обрабатываемый менеджером',
                                 'list_ctrl': u'Объект спискового контрола для отображения списка документов',
                                 'columns': u'Список колонок спискового контрола'
                                 },
                }

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = bmpfunc.createLibraryBitmap('ic_box_doc_navigator.png')
ic_class_pic2 = bmpfunc.createLibraryBitmap('ic_box_doc_navigator.png')

#   Путь до файла документации
ic_class_doc = 'work_flow/doc/_build/html/work_flow.usercomponents.icdocumentnavigatormanager.html'
ic_class_spc['__doc__'] = ic_class_doc

#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = None

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (0, 1, 2, 2)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('document', 'list_ctrl'):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if ret is None:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('document',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('Document', 'NodeDocument', 'BusinessObj', 'StateObj'):
                dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                                       u'Выбранный объект не является документом/бизнес объектом.', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK
        else:
            # Не определена БД
            parent = propEdt
            dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                                   u'Свойство <%s> обязательно должно быть определено для этого объекта.' % attr, parent)
    elif attr in ('list_ctrl',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            parent = propEdt
            if not ret[0][0] in ('ListCtrl', 'Grid'):
                dlgfunc.openWarningBox(u'ВНИМАНИЕ!',
                                       u'Выбранный объект не является списковым контролом', parent)
                return coderror.IC_CTRL_FAILED_IGNORE
            return coderror.IC_CTRL_OK


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('document', 'list_ctrl'):
        return pspEdt.str_to_val_user_property(text, propEdt)


class icDocumentNavigatorManager(icwidget.icSimple,
                                 parentModule.icDocumentNavigatorManagerProto):
    """
    Компонент менеджера навигации документов.

    :type component_spc: C{dictionary}
    :cvar component_spc: Спецификация компонента.

        - B{type='defaultType'}:
        - B{name='default'}:

    """
    component_spc = ic_class_spc

    def __init__(self, parent, id=-1, component=None, logType=0, evalSpace=None,
                 bCounter=False, progressDlg=None):
        """
        Конструктор базового класса пользовательских компонентов.

        :type parent: C{wx.Window}
        :param parent: Указатель на родительское окно.
        :type id: C{int}
        :param id: Идентификатор окна.
        :type component: C{dictionary}
        :param component: Словарь описания компонента.
        :type logType: C{int}
        :param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        :param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        :type evalSpace: C{dictionary}
        :type bCounter: C{bool}
        :param bCounter: Признак отображения в ProgressBar-е. Иногда это не нужно -
            для создания объектов полученных по ссылки. Т. к. они не учтены при подсчете
            общего количества объектов.
        :type progressDlg: C{wx.ProgressDialog}
        :param progressDlg: Указатель на идикатор создания формы.
        """
        component = util.icSpcDefStruct(self.component_spc, component)
        icwidget.icSimple.__init__(self, parent, id, component, logType, evalSpace)

        # Родительский класс icDocumentNavigatorManagerProto не имеет конструктора.
        # Вызывать конструктор не нужно
        # parentModule.icDocumentNavigatorManagerProto.__init__(self, parent)

        # Свойства компонента
        #   По спецификации создаем соответствующие атрибуты (кроме служебных атрибутов)
        lst_keys = [x for x in component.keys() if x.find('__') != 0]

        for key in lst_keys:
            setattr(self, key, component[key])

        #   Создаем дочерние компоненты
        if 'child' in component:
            self.childCreator(bCounter, progressDlg)

        # Инициализация документа
        doc_psp = self.getDocumentPsp()
        if doc_psp:
            self.setSlaveDocumentByPsp(doc_psp, bAutoUpdate=False)
        else:
            log.warning(u'Не определен паспорт ведомого документа для менеджера навигации <%s>' % self.getName())

        # Инициализация контрола списка
        list_ctrl_psp = self.getListCtrlPsp()
        if list_ctrl_psp:
            self.setSlaveListCtrlByPsp(list_ctrl_psp)
        else:
            log.warning(u'Не определен паспорт ведомого контрола списка для менеджера навигации <%s>' % self.getName())

        # Инициализация колонок
        columns = self.getColumns()
        if columns and (isinstance(columns, list) or isinstance(columns, tuple)):
            self.setDocListCtrlColumns(*columns)
        else:
            log.warning(u'Не определен список колонок ведомого контрола списка для менеджера навигации <%s>' % self.getName())

    def childCreator(self, bCounter, progressDlg):
        """
        Функция создает объекты, которые содержаться в данном компоненте.
        """
        return prs.icResourceParser(self, self.resource['child'], None, evalSpace=self.evalSpace,
                                    bCounter=bCounter, progressDlg=progressDlg)

    def getDocumentPsp(self):
        """
        Паспорт управляемого документа.
        """
        return self.getICAttr('document')

    def getListCtrlPsp(self):
        """
        Паспорт управляемого контрола списка.
        """
        return self.getICAttr('list_ctrl')

    def getColumns(self):
        """
        Список описания колонок.
        """
        return self.getICAttr('columns')
