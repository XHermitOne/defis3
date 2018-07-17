#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль функций генерации модулей Python.
"""

# Подключение библиотек
import os
import os.path
import inspect
import wx

from ic.log import log
from ic.dlg import ic_dlg
from . import ic_extend
from . import util
from . import ic_str


# Формат для генерации текста модуля формы
GEN_PY_MODULE_FMT = u'''#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Модуль формы <%s>. 
Сгенерирован проектом DEFIS по модулю формы-прототипа wxFormBuider.
\"\"\"

import wx
import %s

import ic
from ic.log import log

# Для управления взаимодействия с контролами wxPython
# используется менеджер форм <form_manager.icFormManager>
from ic.engine import form_manager


class %s(%s.%s, form_manager.icFormManager):
    \"\"\"
    Форма .
    \"\"\"
    def __init__(self, *args, **kwargs):
        \"\"\"
        Конструктор.
        \"\"\"
        %s.%s.__init__(self, *args, **kwargs)

    def init(self):
        \"\"\"
        Инициализация панели.
        \"\"\"
        self.init_img()
        self.init_ctrl()
        
    def init_img(self):
        \"\"\"
        Инициализация изображений.
        \"\"\"
        pass
        
    def init_ctrl(self):
        \"\"\"
        Инициализация контролов.
        \"\"\"
        pass
        
%s
%s
'''

SHOW_PANEL_FUNC_BODY_FMT = u'''
def %s(title=u''):
    \"\"\"
    @param title: Заголовок страницы нотебука главного окна.
    \"\"\"
    main_win = ic.getMainWin()
        
    panel = %s(main_win)
    panel.init()
    main_win.AddPage(panel, title)    
'''


SHOW_DIALOG_FUNC_BODY_FMT = u'''
def %s(parent=None):
    \"\"\"
    @param parent: Родительское окно.
    @return: True/False.
    \"\"\"
    if parent is None:
        parent = ic.getMainWin()

    dlg = %s(parent)
    dlg.init()
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        return True
    return False
'''


def genPyForm_by_wxFBModule(wxFB_module_filename, output_filename=None,
                            src_class_name=None, parent=None, re_write=False):
    """
    Генерация модуля формы по модулю формы, сгенерированного wxFormBuilder. 
    @param wxFB_module_filename: Полное наименование файла модуля Python,
        сгенерированного wxFormBuilder.
    @param output_filename: Имя результирующего файла.
        Новый файл генерируется в той же папке, что и исходный, 
        если не указано полное наименование выходного файла.
    @param src_class_name: Имя класса формы-источника дя генерации. 
        Если не указано, то функция предлагает выбрать из существующих.
    @param parent: Родительское окно для диалоговых окон.
    @param re_write: Произвести перезапись результирующего файла-модуля, 
        если он уже существует? 
        ВНИМАНИЕ! Перезапись необходимо производить только в крайних случаях, т.к.
        можно затереть изменения в файлах.
    @return: Имя результирующего файла или None, если произошла ошибка генерации.  
    """
    if not os.path.exists(wxFB_module_filename):
        log.warning(u'Генерация Python модуля. Файл <%s> не существует' % wxFB_module_filename)
        return None

    try:
        src_module_name = os.path.splitext(os.path.basename(wxFB_module_filename))[0]
        src_module_path = os.path.dirname(wxFB_module_filename)
        fb_module = util.icLoadSource(src_module_name, wxFB_module_filename)
        fb_module_classes = [var_name for var_name in dir(fb_module) if inspect.isclass(getattr(fb_module, var_name))]
        log.debug(u'Найденные классы %s в модуле <%s>' % (fb_module_classes, wxFB_module_filename))

        if src_class_name is None:
            if len(fb_module_classes) == 1:
                # У нас одна форма по ней и генерируем
                src_class_name = fb_module_classes[0]
            else:
                # У нас несколько форм необходимо предложить выбрать
                choices = [frm_class_name for frm_class_name in fb_module_classes]
                choices.sort()
                src_class_name = ic_dlg.icSingleChoiceDlg(Parent_=parent, Title_=u'wxFormBuilder',
                                                          Text_=u'Выберите протоотип форма/панели wxFormBuilder для источника генерации:',
                                                          Choice_=choices)

        if output_filename is None:
            # Если имя выходного файла не определено, то
            # генерируем имя файла из имени класса формы
            dst_module_name = src_class_name
            dst_module_name = dst_module_name[2:] if dst_module_name.startswith('ic') else dst_module_name
            dst_module_name = dst_module_name[:-9] if dst_module_name.endswith('Prototype') else dst_module_name
            dst_module_name = dst_module_name[:-5] if dst_module_name.endswith('Proto') else dst_module_name
            dst_module_name = ic_str.upper_symbols2_lower(dst_module_name)

            output_filename = os.path.join(src_module_path, '%s.py' % dst_module_name)

        if os.path.exists(output_filename) and re_write:
            # Удаляем результирующий файл
            os.remove(output_filename)
            log.info(u'Файл модуля Python <%s> удален' % output_filename)

        if not os.path.exists(output_filename):
            # Генерацию производим только если результирующего файла нет,
            # что бы не потерять ранее внесенные изменения в файле
            dst_class_name = src_class_name
            dst_class_name = dst_class_name[:-9] if dst_class_name.endswith('Prototype') else dst_class_name
            dst_class_name = dst_class_name[:-5] if dst_class_name.endswith('Proto') else dst_class_name
            src_class = getattr(fb_module, src_class_name)

            src_class_methods = [getattr(src_class, var_name) for var_name in dir(src_class)]
            src_class_events = [method for method in src_class_methods if inspect.ismethod(method) and
                                method.__name__ != '__init__' and
                                'event' in method.func_code.co_varnames and
                                method.func_code.co_argcount == 2]
            # Способ получения исходного кода из объекта функции-+
            #                                                    v
            body_functions = u'\n'.join([u'\n'.join(inspect.getsourcelines(class_method)[0]) for class_method in src_class_events])
            body_functions = body_functions.replace(u'\t', u'    ').replace(u'( ', u'(').replace(u' )', u')')

            # Функция вызова формы
            frm_body_function = u''
            frm_function_name = 'show_%s' % ic_str.upper_symbols2_lower(dst_class_name[2:] if dst_class_name.startswith('ic') else dst_class_name)
            if issubclass(src_class, wx.Panel):
                frm_body_function = SHOW_PANEL_FUNC_BODY_FMT % (frm_function_name, dst_class_name)
            elif issubclass(src_class, wx.Dialog):
                frm_body_function = SHOW_DIALOG_FUNC_BODY_FMT % (frm_function_name, dst_class_name)
            else:
                log.warning(u'Не поддерживаемый тип для генерации функции вызова формы <%s>' % src_class.__name__)

            py_txt = GEN_PY_MODULE_FMT % (src_class_name,
                                          src_module_name,
                                          dst_class_name, src_module_name, src_class_name,
                                          src_module_name, src_class_name,
                                          body_functions,
                                          frm_body_function)
            log.debug(u'Сохранение файла <%s>' % output_filename)
            result = ic_extend.save_file_text(output_filename, py_txt)
            if result:
                return output_filename
            else:
                log.warning(u'Ошибка сохранения файла <%s>' % output_filename)
        else:
            msg = u'Файл модуля python <%s> уже существует. Генерация не возможна' % output_filename
            log.warning(msg)
            ic_dlg.icWarningBox(u'ВНИМАНИЕ!', msg)
    except:
        log.fatal(u'Ошибка генерации модуля формы по модулю формы, сгенерированного wxFormBuilder')
    return None
