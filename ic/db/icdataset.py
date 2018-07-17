#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Базовый класс для работы с табличными данными.
Модуль содержит описание класса ссылки и функций для поиска по дереву ресурса.

@var icTextFieldType: Идентификатор текстового типа поля.
@var icNumberFieldType: Идентификатор целого типа поля.
@var icDoubleFieldType: Идентификатор вещественного типа поля.
@var icDateTimeFieldType: Идентификатор дата-время типа.
@var icNormalFieldType: Идентификатор поля базы данных.
@var icVirtualFieldType: Идентификатор вычислимого поля.

@type SPC_IC_DATALINK: C{Dictionary}
@var SPC_IC_DATALINK: Спецификация на ресурсное описание ссылки на объект. Созданный по ссылке объект
в пространстве имен формы будет иметь имя ссылки. Описание ключей:

    - B{name = 'Link'}: Имя объекта источника данных. В форме используется как алиас источника данных
    - B{type='DataLink'}: Тип объекта.
    - B{filter=None}: Фильтр на объект данных. Если словарь, то фильтр на значение поля. Если строка, то фильтрация
        проводится по SQL выражению, записанному в данном атрибуте.
        Пример 1: {'cod':'001','typ':0}
        Пример 2: 'select id from analitic where reg='0241''
        Пример 3: 'reg>'0241' and reg>'0250'' - пока не работает
    - B{res_query=''}: Имя либо выражение(возвращающее имя) нужного объекта ресурсного описания.
        Выражение определяется по символу '@'.
        Формат описания:
        <Имя ресурса>:<Тип компонента>.<Имя компонента>
    - B{link_expr=None}: Выражение, выполняемое после нахождения ресурсного описания.
    - B{file=None}: Путь до файла ресурса. Пример: 1 - 'table.tab'; 2 - 'NSI/resource.tab'; 3 - 'c:/defis/balans/balans/account.tab'.
    - B{_uuid=None}: Уникальный идентификатор ссылки.
    - B{<Дополнительные параметры>}: Дополнительные параметры задают переопределяемые атрибуты
        ресурсного описания. Имя переопределяемого атрибута задается в виде
        B{Тип объекта:имя объекта:имя аттрибута}, в качестве значения - новое значение атрибута.
        Все переопределяемые атрибуты могут быть вычисляемыми. Признаком вычисляемого атрибута является
        символ '@'.
"""

# import wx
# import sys
# import os
# import copy
# import string
# import ic
import ic.utils.resource as resource
from ic.utils.util import icSpcDefStruct, ic_eval
import ic.utils.util as util

# from ic.log.iclog import MsgLastError
# from ic.dlg.msgbox import MsgBox
from ic.dlg import ic_dlg
from ic.utils import ic_uuid
from ic.kernel import io_prnt
from ic.utils import coderror
import ic.PropertyEditor.icDefInf as icDefInf
from ic.PropertyEditor.ExternalEditors.passportobj import icObjectPassportUserEdt as pspEdt
from ic.components import icwidget

# ---- Идентификаторы типов полей ----
#   Текстовый тип
icTextFieldType = 1
#   Целый числовой
icNumberFieldType = 2
#   Вещественный
icDoubleFieldType = 3
#   Дата - время
icDateTimeFieldType = 4

# ---- Идентификаторы атрибутов полей ----
#       Поле базы данных
icNormalFieldType = 0
#       Вычисляемое поле
icVirtualFieldType = 1
#       Поле базы данных, только для чтеня
icNormalReadOnlyFieldType = 2
#       Вычисляемое поле, только для чтеня
icVirtualReadOnlyFieldType = 3

#   Путь до папки ресурсов по умолчанию
IC_DATACLASS = '.\\res\\resource.tab'

SPC_IC_DATALINK = {'name': 'Link',
                   'type': 'DataLink',
                   'alias': None,
                   'activate': True,
                   'init_expr': None,
                   '_uuid': None,

                   'res_query': '',
                   'file': '',
                   'link_expr': None,
                   'filter': None,
                   'docstr': 'ic.db.icdataset-module.html',
                   'psp_link': None,    # Связь с ресурсом по паспорту

                   '__attr_types__': {icDefInf.EDT_PY_SCRIPT: ['filter', 'link_expr', 'init_expr'],
                                      icDefInf.EDT_TEXTFIELD: ['res_query', 'file', 'name',
                                                               'type', '_uuid', 'alias'],
                                      icDefInf.EDT_CHECK_BOX: ['activate'],
                                      icDefInf.EDT_USER_PROPERTY: ['psp_link'],
                                      },
                   '__parent__': icwidget.SPC_IC_SIMPLE,
                   '__attr_hlp__': {'psp_link': u'Связь с ресурсом по паспорту',
                                    },
                   }

# ---- Общий интерфэйс модуля

#   Тип компонента. None, означает, что данный компонент убран из
#   редактора и остался только для совместимости со старыми проектами.
ic_class_type = icDefInf._icServiceType

#   Имя пользовательского класса
ic_class_name = 'icDataLink'

#   Описание стилей компонента
ic_class_styles = None

#   Спецификация на ресурсное описание пользовательского класса
ic_class_spc = SPC_IC_DATALINK
ic_class_spc['__styles__'] = ic_class_styles

#   Имя иконки класса, которые располагаются в директории
#   ic/components/user/images
ic_class_pic = '@common.imgEdtDataLink'
ic_class_pic2 = '@common.imgEdtDataLink'

#   Путь до файла документации
ic_class_doc = None
                    
#   Список компонентов, которые могут содержаться в компоненте
ic_can_contain = []

#   Список компонентов, которые не могут содержаться в компоненте, если не определен
#   список ic_can_contain
ic_can_not_contain = None

#   Версия компонента
__version__ = (1, 0, 2, 1)


# Функции редактирования
def get_user_property_editor(attr, value, pos, size, style, propEdt, *arg, **kwarg):
    """
    Стандартная функция для вызова пользовательских редакторов свойств
    (EDT_USER_PROPERTY).
    """
    ret = None
    if attr in ('psp_link',):
        ret = pspEdt.get_user_property_editor(value, pos, size, style, propEdt)

    if not ret:
        return value

    return ret


def property_editor_ctrl(attr, value, propEdt, *arg, **kwarg):
    """
    Стандартная функция контроля.
    """
    if attr in ('psp_link',):
        ret = str_to_val_user_property(attr, value, propEdt)
        if ret:
            # В качестве объекта-источника может выступать любой объект
            return coderror.IC_CTRL_OK
        return coderror.IC_CTRL_FAILED


def str_to_val_user_property(attr, text, propEdt, *arg, **kwarg):
    """
    Стандартная функция преобразования текста в значение.
    """
    if attr in ('psp_link',):
        return pspEdt.str_to_val_user_property(text, propEdt)


def findResPath(res, path, i=0):
    """
    Функция рекурсивно по заданному пути находит нужное ресурсное описание. Путь задается списком имен наследования.
    Любое ресурсное описание в обезательном порядке имеет ключ 'name', по этому имени и ведется поиск нужного
    описания. Наследование задается через список, с ключом 'child'.
        
    @type res: C{dictionary}
    @param res: Ресурсное описание, в котором ищется описание нужного компонента.
    @type path: C{list}
    @param path: Путь до нужного описания.

        - B{Пример:} C{['Frame1','Split1','Win1','button5']}

    @type i: C{int}
    @param i: Номер имени в списке, описывающем путь до ремурсного описания.
    @rtype: C{dictionary}
    @return: Возвращает нужное ресурсное описание если находит и C{None}, если не находит.
    """
    
    if i >= len(path):
        return None
    
    if (res['name'] == path[i] and i == len(path) - 1) or path[i] == '':
        return res
    
    elif res['name'] != path[i]:
        return None
    
    elif 'scheme' in res:
        
        for obj_res in res['scheme']:
            if i + 1 < len(path) and obj_res['name'] == path[i+1]:
                ret = findResPath(obj_res, path, i+1)
    
                if ret is not None:
                    return ret

    elif 'group' in res:
        
        for obj_res in res['group']:
            if i + 1 < len(path) and obj_res['name'] == path[i+1]:
                ret = findResPath(obj_res, path, i+1)
    
                if ret is not None:
                    return ret
    
    elif 'child' in res:
        
        for obj_res in res['child']:
            if i + 1 < len(path) and obj_res['name'] == path[i+1]:
                ret = findResPath(obj_res, path, i+1)
    
                if ret is not None:
                    return ret
            
    elif 'items' in res:
        
        for obj_res in res['items']:
            if i + 1 < len(path) and obj_res['name'] == path[i+1]:
                ret = findResPath(obj_res, path, i+1)
    
                if ret is not None:
                    return ret
            
    if 'win1' in res:
        
        if i + 1 < len(path)  and res['win1']['name'] == path[i+1]:
            ret = findResPath(res['win1'], path, i+1)
    
            if ret is not None:
                return ret
            
    if 'win2' in res:
        
        if i + 1 < len(path) and res['win2']['name'] == path[i+1]:
            ret = findResPath(res['win2'], path, i+1)
    
            if ret is not None:
                return ret
        
    return None


def findResName(res, name):
    """
    Функция по имени ищет ресурсное описание рекурсивно обходя все дерево ресурсного описания. Любое ресурсное
    описание в обезательном порядке имеет ключ 'name', по этому имени и ведется поиск нужного описания.
    Наследование задается через список, с ключом 'child' и аттрибуты с ключами 'Win1' и 'Win2', которые
    используются при описании компонента icSplitter.
    
    @type res: C{dictionary}
    @param res: Ресурсное описание, в котором ищется описание нужного компонента.
    @type name: C{string}
    @param name: Имя объекта описание, которого ищет функция.
    @rtype: C{dictionary}
    @return: Возвращает нужное ресурсное описание, если находит и C{None}, если не находит.
    """

    if res['name'] == name:
        return res
    
    elif 'child' in res:
        
        for obj_res in res['child']:
            ret = findResName(obj_res, name)
    
            if ret is not None:
                return ret
    
    elif 'items' in res:
        
        for obj_res in res['items']:
            ret = findResName(obj_res, name)
    
            if ret is not None:
                return ret
    
    if 'win1' in res:
        ret = findResName(res['win1'], name)
    
        if ret is not None:
            return ret
            
    if 'win2' in res:
        ret = findResName(res['win2'], name)
    
        if ret is not None:
            return ret
    
    return None


def findResQuery(res, xpath):
    """
    Функция по запросу находит нужное ресурсное описание.
    
    @type res: C{dictionary}
    @param res: Ресурсное описание, в котором ищется описание нужного компонента.
    @type xpath: C{string}
    @param xpath: Запрос на нужный компонент. '/' указывает на путь наследование; '//' указывает на рекурсивный
        поиск нужного описания. Примеры:
        
            - C{'Frame1/panel1/split1/Win1/sizer1/button1'} - запрос с указанием полного пути до описания 'button1'.
            - C{'//button1'} - запрос на поиск с указанием только имени нужного описания.
            - C{'Frame1/panel1/split1//button1'} - запрос на поиск с указанием пути до компонента split1 и именем
                нужного описания.

    @rtype: C{dictionary}
    @return: Возвращает нужное ресурсное описание если находит и C{None}, если не находит.
    """
    lxpath = xpath.split('//')
    
    if len(lxpath) > 1:
        i = 0
        
        for spath in lxpath:
            path = spath.split('/')
            
            if len(path) > 1:
                res = findResPath(res, path)
            
            if i+1 < len(lxpath):
                path_next = lxpath[i+1].split('/')
                res = findResName(res, path_next[0])

            i += 1
    else:
        res = findResPath(res, lxpath[0])
        
    return res


def findResTypeLst(res, typRes, lst=None):
    """
    Функция возвращет список ресурсов заданного типа. Поиск ведется рекурсивно
    по ресурсу.
    
    @type res: C{dictionary}
    @param res: Ресурсное описание, где происходить поиск.
    @type typRes: C{string}
    @param typRes: Тип ресурса, который ищется.
    @rtype: C{list}
    @return: Возвращет список ресурсов заданного типа.
    """
    if not res or not isinstance(res, dict):
        return lst
    
    if lst is None:
        lst = []
    
    if 'type' in res and res['type'] == typRes:
        lst.append(res)
    
    if 'child' in res and type(res['child']) in (list, tuple):
        for r in res['child']:
            lst = findResTypeLst(r, typRes, lst)
    elif 'cols' in res and type(res['cols']) in (list, tuple):
        for r in res['cols']:
            lst = findResTypeLst(r, typRes, lst)
    elif 'win1' in res and type(res['win1']) in (list, tuple):
        for r in res['win1']:
            lst = findResTypeLst(r, typRes, lst)
    elif 'win2' in res and type(res['win2']) in (list, tuple):
        for r in res['win2']:
            lst = findResTypeLst(r, typRes, lst)
        
    return lst


def setResAttr(res, typRes, name, attr, value, uuidLink=None, prntRes=None):
    """
    Функция ищет в ресурсе ресурс заданного типа и имени и устанавливает значение
    заданного атрибута. При этом генерируется новый UUID ресурса - половинка старого UUID
    складывается с половинкой ссылки.
    
    @type res: C{dictionary}
    @param res: Ресурсное описание, где происходить поиск.
    @type typRes: C{string}
    @param typRes: Тип ресурса, который ищется.
    @type name: C{string}
    @param name: Имя ресурного описаия компонента.
    @type attr: C{string}
    @param attr: Имя атрибута.
    @type value: C{...}
    @param value: Новое значение атрибута.
    @type uuidLink: C{string}
    @param uuidLink: Универсальный идентификатор ссылки.
    @type prntRes: C{dictionary}
    @param prntRes: Ресурсное описание родительского компонента-контейнера.
    @rtype: C{bool}
    @return: Признак того, что нужный атрибут найден и установлен. None означает,
        что компонет не имеет нужного атрибута.
    """
    if not isinstance(res, dict) or not res:
        return False
    
    #   Если нужный компонент нашли пытаемся установить атрибут
    res_name = None
    
    if 'type' in res and 'name' in res and res['type'] == typRes:
        if 'alias' in res and not res['alias'] in [None, '', 'None']:
            res_name = res['alias']
        else:
            res_name = res['name']

    if res_name == name:
        try:
            res[attr] = value
            
            if res['type'] == 'GridCell' and prntRes and uuidLink and '_uuid' in prntRes:
                nf = len(uuidLink)/2
                prntRes['_uuid'] = prntRes['_uuid'][:nf]+uuidLink[nf:]
                
            elif uuidLink and '_uuid' in res:
                nf = len(uuidLink)/2
                res['_uuid'] = res['_uuid'][:nf]+uuidLink[nf:]
                
            return True
        except:
            io_prnt.outLastErr(u'setResAttr ERROR')
            return None
    else:
        for key in res:
            #   Если значение атрибута словарь
            if isinstance(res[key], dict):
                bret = setResAttr(res[key], typRes, name, attr, value, uuidLink, res)
                
                if bret is None or bret:
                    return bret
                
            #   Если значение атрибута список
            elif isinstance(res[key], list):
                
                for r in res[key]:
                    if isinstance(r, dict):
                        bret = setResAttr(r, typRes, name, attr, value, uuidLink, res)
                
                        if bret is None or bret:
                            return bret
    return False


def getRes(res, typRes, name):
    """
    Функция ищет в ресурсе ресурс заданного типа и имени и возвращает его.
    
    @type res: C{dictionary}
    @param res: Ресурсное описание, где происходить поиск.
    @type typRes: C{string}
    @param typRes: Тип ресурса, который ищется.
    @type name: C{string}
    @param name: Имя ресурного описаия компонента.
    @rtype: C{tuple}
    @return: Возвращает найденный ресурс
    """
    if isinstance(res, dict) or not res:
        return False
    
    #   Если нужный компонент нашли пытаемся установить атрибут
    res_name = None
    
    if 'type' in res and 'name' in res and res['type'] == typRes:
        if 'alias' in res and not res['alias'] in [None, '', 'None']:
            res_name = res['alias']
        else:
            res_name = res['name']

    if res_name == name:
        return res
    
    else:
        for key in res:
            #   Если значение атрибута словарь
            if isinstance(res[key], dict):
                bret = getRes(res[key], typRes, name)
                
                if bret:
                    return bret
                
            #   Если значение атрибута список
            elif isinstance(res[key], list):
                
                for r in res[key]:
                    if isinstance(r, dict):
                        bret = getRes(r, typRes, name)
                    
                        if bret:
                            return bret
    return False

#   Список атрибутов контейнеров
contAttr = ['child', 'cols', 'win1', 'win2']


class icDataLink(icwidget.icSimple):
    """
    Класс объекта ссылки на ресурсное описание.
    """
    
    def __init__(self, component={}, logType=0, evalSpace=None, bDefSearch=True, fltDict=None):
        """
        Конструктор для создания ссылки.

        @type component: C{dictionary}
        @param component: Словарь описания компонента.
        @type logType: C{int}
        @param logType: Тип лога (0 - консоль, 1- файл, 2- окно лога).
        @param evalSpace: Пространство имен, необходимых для вычисления внешних выражений.
        @type evalSpace: C{dictionary}
        @type bDefSearch: C{bool}
        @param bDefSearch: Используется если в пространстве имен нужный объект не обнаружен. Признак определяет искать ли нужное
            ресурсное описание в ресурсных файлах по умолчанию (./res/resource.tab).
        @type fltDict: C{dictionary}
        @param fltDict: Словарь заменяемых фильтров у источников данных.
        """
        icwidget.icSimple.__init__(self, parent=None, component=component,
                                   logType=logType, evalSpace=evalSpace)
        # self.evalSpace = evalSpace
        # self.logType = logType
        self.obj = None

        if fltDict:
            self.fltDict = fltDict
        else:
            self.fltDict = {}
            
        icSpcDefStruct(SPC_IC_DATALINK, component)

        self._component = component
        self.name = component['name']
        self.source = util.getSpcAttr(component, 'file', evalSpace).strip()
        self._uuid = component['_uuid']
        
        if not self._uuid:
            self._uuid = ic_uuid.get_uuid()

        self.resource = self.GetResource(component)
        
    def GetExtAndPathSource(self, source):
        """
        По атрибуту <source> определяется имя и расширение файла ресурса.

        @type source: C{string}
        @param source: Значение атрибута источника.
        @rtype: C{tuple}
        @return: Возвращает картеж первый элемент - путь, второй - имя, третий -
            расширение файла ресурса.
        """

        path = None
        res_ext = 'tab'
        nameRes = 'resource'

        if source:
            source = source.replace('\\', '/')
            sys_path = resource.icGetSubsysResPaths()[0].replace('\\', '/')
            
            #   Если указан полный путь до файла
            #   <C:/Projects/NSI/NSI/sprav.tab>
            #   <C:/Projects/DOCT/NSI/sprav.tab>
            if ':' in source and '.' in source:
                path = '/'.join(source.split('/')[:-1])
                nameRes = source.split('/')[-1].split('.')[0]
                res_ext = source.split('.')[-1]
                
            #   Если указан полный путь до папки
            #   <C:/Projects/NSI/NSI>
            elif ':' in source:
                path = source
                                
            #   Если относительный путь до файла c указанием подсистемы
            #   <NSI/sprav.tab>
            elif '/' in source and '.' in source:
                path = ('/'.join(sys_path.split('/')[:-1]) +
                        '/'+'/'.join(source.split('/')[:-1]))
                nameRes = source.split('/')[-1].split('.')[0]
                res_ext = source.split('.')[-1]
                
            #   Если относительный путь до файла без указания папки
            #   <sprav.tab>
            elif '.' in source:
                res_ext = source.split('.')[-1]
                nameRes = source.split('.')[0]

            #   Если указан относительный путь до папки подсистемы
            #   <NSI>
            else:
                path = '/'.join(sys_path.split('/')[:-1])+'/'+source
                
        return path, nameRes, res_ext

    def GetResource(self, component):
        """
        Собирает ресурсное описание по ссылке.

        @type component: C{dictionary}
        @param component: Словарь описания ссылки.
        """
        if 'psp_link' in component and component['psp_link']:
            return self.getResourceByPspLink(component)
        if 'link_expr' in component and component['link_expr']:
            return self.getResourceByLinkExpr(component)
        return self.getResourceByFileLink(component)

    def getResourceByLinkExpr(self, component):
        """
        Определить ресурс по выражению.
        Если не определен ресурс и определено выражение, которое возвращает
        ресурс.
        @return:
        """
        res = None
        link_expr = component['link_expr']
        self.evalSpace['self'] = self
        ret, val = ic_eval(link_expr, 0, self.evalSpace, 'icDataLink <link_expr>',
                           compileKey=ic_uuid.get_uuid_attr(self._uuid, 'link_expr'))
        if ret:
            if isinstance(val, dict) and 'name' in val and 'type' in val:
                res = val
                res['alias'] = component['name']
        return res

    def doReplacementRes(self, res, component):
        """
        Произвести замены в ресурсе.
        Замены производяться с помощью метода <ReloadAttr>.
        @param res: Ресурс.
        @param component: Описание компонента DataLink.
        @return: Ресурс с произведенными заменами.
        """
        contKeys = [x for x in res.keys() if x in contAttr]

        for key in contKeys:
            #   Если атрибут является контейнером описаний, выбираем
            #   из него описание ссылок
            if isinstance(res[key], list):
                for indx, comp in enumerate(res[key]):
                    if comp['type'] == 'DataLink':
                        new_res = self.GetResource(comp)
                        res[key][indx] = new_res

        # По необходимости перегружаем атрибуты ресурсного описания
        res = self.ReloadAttr(res, component)

        #   Заменяем имя источника данных на имя ссылки. Это позволит
        #   использовать для разных компонентов, по-разному отфильтрованный,
        #   один один и тотже класс данных.
        name = component['name']
        res['alias'] = name

        #   Устанавливаем фильр на источник данных из описания объекта
        #   ссылки (icDataLink) либо из буффера замен self.fltDict.
        #   Буффер заполняется в функции, которая вызывает текущую ф-ию
        if res['type'] in ['icDataClass', 'icQuery', 'Table']:

            if name in self.fltDict:
                res['filter'] = self.fltDict[name]
                io_prnt.outLog(u'RELOAD FILTER IN DATALINK <%s> [%s]' % (name, res['filter']))
            else:
                res['filter'] = component['filter']
        return res

    def getResourceByPspLink(self, component):
        """
        Собирает ресурсное описание по ссылке.
        Ресурсное описание собирается по паспорту объекта.
        @type component: C{dictionary}
        @param component: Словарь описания ссылки.
        """
        res = None
        res_query = util.getSpcAttr(component, 'res_query', self.evalSpace).strip()
        psp_link = component['psp_link']

        _query = res_query.split(':')

        try:
           link_type = _query[1].split('.')[0]
           link_name = _query[1].split('.')[1]

           io_prnt.outLog(u'ICDATASET: point to object resource: type=<%s>, name=<%s>' % (link_type, link_name))
        except:
           link_type = None
           link_name = None

        #   Получаем ресурсное описание, где в общем случае ищется
        #   описание нужного компонента
        io_prnt.outLog(u'Связь с ресурсом по паспорту: %s' % psp_link)
        res = resource.getResByPsp(psp_link)

        # ---- В ресурсе ищем описание нужного компoнента
        #   (<key_in_fileres>:type.name)
        if link_name and link_type:
            ret = getRes(res, link_type, link_name)

            if not ret:
                io_prnt.outWarning(u'Не найден объект [%s : %s] в ресурсе' % (link_type, link_name))
                res = None

        # -------------------------------------------------------------
        #   В полученном ресурсном описании ищем ссылки и заменяем их
        #   на ресурсные описания
        if res:
            res = self.doReplacementRes(res, component)
        else:
            # Если ресурсное описание не найдено и выражение изменений не
            #   определено, то сообщаем об этом пльзователю
            ic_dlg.icWarningBox(u'ОШИБКА', u'Описание объекта <%s> в %s не найдено.' % (res_query, psp_link))

        return res

    def getResourceByFileLink(self, component):
        """
        Собирает ресурсное описание по ссылке.
        Ресурсное описание собирается по ссылке на файл ресурса.
        @type component: C{dictionary}
        @param component: Словарь описания ссылки.
        """
        res = None
        name = component['name']
        source = util.getSpcAttr(component, 'file', self.evalSpace).strip()
        res_query = util.getSpcAttr(component, 'res_query', self.evalSpace).strip()
        link_expr = component['link_expr']

        #   Если не определен ресурс и определено выражение, которое возвращает
        #   ресурс
        if not source and not res_query and component['link_expr']:
            return self.getResourceByLinkExpr(component)

        _query = res_query.split(':')
        link_key = _query[0]
        
        try:
            link_type = _query[1].split('.')[0]
            link_name = _query[1].split('.')[1]
            
            io_prnt.outLog(u'ICDATASET: point to object resource: type=<%s>, name=<%s>' % (link_type, link_name))
        except:
            link_type = None
            link_name = None

        # Определяем тип и путь до ресурсного файла ---------------
        path, nameRes, res_ext = self.GetExtAndPathSource(source)
            
        #   Получаем ресурсное описание, где в общем случае ищется
        #   описание нужного компонента
        if link_key:
            
            try:
                io_prnt.outLog(u'DATA LINK TO key=%s, path=%s, ext=%s' % (link_key, path, res_ext))
                res = resource.icGetRes(link_key, res_ext, path, nameRes=nameRes)
                                
                #   В описание найденого ресурса добавляем атрибуты, которые
                #   описывают файл ресурса
                res['__subsys_path'] = path
                res['__resource_ext'] = res_ext
                
            except IOError:
                ic_dlg.icWarningBox(u'ОШИБКА', u'Ошибка открытия файла %s.' % source)
                
        # ---- В ресурсе ищем описание нужного компанента
        #   (<key_in_fileres>:type.name)
        if link_name and link_type:
            ret = getRes(res, link_type, link_name)
            
            if ret:
                res = ret
            else:
                res = None
        
        #   Если определено выражение, возвращающее ресурсное описание,
        # выполняем его
        if link_expr:
            
            self.evalSpace['self'] = self
            ret, val = ic_eval(link_expr, 0, self.evalSpace, 'icDataLink <link_expr>',
                               compileKey=ic_uuid.get_uuid_attr(self._uuid, 'link_expr'))
            
            if ret:
                if isinstance(val, dict) and 'name' in val and 'type' in val:
                    res = val
                    io_prnt.outLog(u'ICDATASET RCONSTRUCT RES: <%s>' % val)

        # -------------------------------------------------------------
        #   В полученном ресурсном описании ищем ссылки и заменяем их
        #   на ресурсные описания
        if res:
            res = self.doReplacementRes(res, component)

        #   Если ресурсное описание не найдено и выражение изменений не
        #   определено, то сообщаем об этом пльзователю
        else:
            ic_dlg.icWarningBox(u'ОШИБКА', u'Описание объект \'%s\' в ресурсном файле \'%s\' не найдено.' % (res_query,
                                                                                                             source))

        return res
    
    def ReloadAttr(self, res, component):
        """
        Перегружает нужные атрибуты ресурсного описания.

        @type res: C{dictionary}
        @param res: Ресурсное описание, в котором заменяются атрибуты.
        @type component: C{dictionary}
        @param component: Ресурсное описание ссылки.
        """
        attrs = getAddProperyLst(SPC_IC_DATALINK, component.keys(),
                                 icDefInf.icUnSpecAttr)

        #   Атрибуты начинающиеся с '__' являются служебными и не обрабатываются
        attrs = [x for x in attrs if x.find('__') != 0]

        #   Переопределяем аттибуты компонента класса данных
        for attr in attrs:
                
            reload_attr = util.getICAttr(component[attr], self.evalSpace)
                
            #   Если дополнительный атрибут задан в виде <typ:name.attr>, то
            #   используем для переопределения атрибута дерева специальную
            #   функцию.
            if ':' in attr and '.' in attr:
                div = attr.split(':')
                name, prp = div[-1].split('.')
                    
                if setResAttr(res, div[0], name, prp, reload_attr, self._uuid):
                    io_prnt.outLog(u'setResAttr() [%s : %s : %s]' % (div[0], name, prp))
            else:
                if attr in res:
                    res[attr] = reload_attr
                else:
                    io_prnt.outWarning(u'RELOAD ATTRIBUTE ERROR in icdataset.icDataLink.__init__(...): Invalid attribute name <%s> in component name:%s' % (attr, component['name']))

        return res
    
    def getObj(self):
        """
        Возвращает указатель на объект.
        """
        
        return self.obj


SPC_IC_FIELD_DEF = {'type': icTextFieldType,
                    'attr': icNormalFieldType,
                    'init': None,
                    'setvalue': None,
                    'getvalue': None
                    }


def getAddProperyLst(spc, attrs, unSpecAttr):
    """
    Определяет список атрибутов, которые не определяются спецификацией.
    
    @type spc: C{dictionary}
    @param spc: Спецификация на описание компонента.
    @type attrs: C{list}
    @param attrs: Список атрибутов компонента.
    @rtype: C{list}
    @return: Список атрибутов, которые не определяются спецификацией.
    """
    lst_add_prop = []
    
    if spc and isinstance(spc, dict):
        lst_add_prop = [x for x in attrs if not x in spc.keys() and not x in unSpecAttr]
    else:
        io_prnt.outLog(u'TYPE ERROR in getAddPropertyList()')
        
    return lst_add_prop


if __name__ == '__main__':
    pass
