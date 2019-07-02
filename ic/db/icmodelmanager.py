#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс системного менеджера моделей на основе SQLAlchemy.
"""

import os.path
import sqlalchemy
import sqlalchemy.orm

from ic.log import log
from ic.utils import resfunc
from ic.utils import ic_str
from ic.utils import ic_extend

from . import icsqlalchemy
from . import icmodel

__version__ = (0, 1, 1, 1)

# Шаблоны генератора модуля
MODEL_MODULE_TXT_FMT = u'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
Модель: %s.
\"\"\"

from ic.log import log
from ic.db import icmodule
from . import %s

%s
'''

MODEL_CLASS_TXT_FMT = u'''
class %s(icmodule.icBaseModule, %s.%s):
    \"\"\"
    %s
    \"\"\"
    __tablename__ = '%s'
%s  
'''

MODEL_MANAGER_TXT_FMT = u'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
Менеджер модели: %s.
\"\"\"

from ic.log import log
from ic.db import icmodulemanager

class %s(icmodulemanager.icModelManager):
    \"\"\"
    %s
    \"\"\"
    pass            
'''


class icModelManager:
    """
    Класс системного менеджера моделей на основе SQLAlchemy.
    """
    # Cессия модели
    session = None

    def set_session(self, session=None):
        """
        Запомнить сессию.
        """
        self.session = session
        if not self.session:
            log.warning(u'Не определен объект сессии объекта <%s>' % self.__class__.__name__)
        return self

    def create_session(self, db_url=None):
        """
        Создать сессию для организации транзакций при работе с БД.
        @param db_url: URL связи с БД.
        @return: Объект сессии или None в случае ошибки.
        """
        if db_url is None:
            log.warning(u'Не определен URL БД при создании сессии модели')
            return None

        engine = sqlalchemy.create_engine(db_url, echo=False)

        # создание конфигурации класса Session
        Session = sqlalchemy.orm.sessionmaker(bind=engine)

        # создание объекта Session
        self.session = Session()
        return self.session

    def close_session(self, session=None):
        """
        Закрыть сессию.
        ВНИМАНИЕ! Необходимо всегда загрывать сессию после использования
        иначе сервер PostgreSQL не освобождаем связи и происходит
        превышение лимита открытых связей. После превышения лимита
        PostygreSQL сервер отказывает клиентам в обслуживании.
        @param session: Объект сессии.
        @return: True/False.
        """
        if session is None:
            session = self.session

        if session is not None:
            session.close()
            return True
        else:
            log.warning(u'Не определен объект сессии для работы с транзакциями БД')
        return False

    def rollback_session(self, session=None, bAutoClose=False):
        """
        Отмена транзакций.
        @param session: Объект сессии.
        @param bAutoClose: Автоматически закрыть сессию?
        @return: True/False.
        """
        if session is None:
            session = self.session

        if session is None:
            log.warning(u'Не определен объект сессии для работы с транзакциями БД')
            return False

        session.rollback()
        if bAutoClose:
            session.close()
        return True

    def commit_session(self, session=None, bAutoClose=False):
        """
        Подтвердить транзакции.
        @param session: Объект сессии.
        @param bAutoClose: Автоматически закрыть сессию?
        @return: True/False.
        """
        if session is None:
            session = self.session

        if session is None:
            log.warning(u'Не определен объект сессии для работы с транзакциями БД')
            return False

        session.commit()
        if bAutoClose:
            session.close()
        return True

    def genModelModuleByTabRes(self, tab_res_filename=None, dst_module_filename=None):
        """
        Генерация модуля модели по ресурсу таблицы.
        @param tab_res_filename: Полное имя файла ресурса таблицы.
        @param dst_module_filename: Полное имя результирующего файла модуля модели.
            Если не определено, то генерируется.
        @return: True/False.
        """
        try:
            tab_res = resfunc.LoadResource(tab_res_filename)
            tab_name = tab_res.keys()[0]
            tab_spc = tab_res[tab_name]
            model_name = 'ic%sModel' % ic_str.lower_symbols2_upper(tab_name)
            manager_module_name = '%s_manager' % tab_name
            manager_name = 'ic%sModelManager' % ic_str.lower_symbols2_upper(tab_name)

            fields = tab_spc.get('child', list())
            field_lines = list()
            for field_spc in fields:
                field_name = field_spc['name']
                obj_type = field_spc['type']
                if obj_type == icsqlalchemy.FIELD_TYPE:
                    # Это поле
                    length = field_spc['len']
                    type_val = field_spc['type_val']
                    if type_val == icsqlalchemy.TEXT_FIELD_TYPE:
                        if length <= 0:
                            col_type = u'sqlalchemy.Text'
                        elif length == 1:
                            col_type = u'sqlalchemy.CHAR(1)'
                        else:
                            col_type = u'sqlalchemy.String(%d)' % int(length)
                    elif type_val == icsqlalchemy.DATE_FIELD_TYPE:
                        col_type = u'sqlalchemy.Date'
                    elif type_val == icsqlalchemy.INT_FIELD_TYPE:
                        col_type = u'sqlalchemy.Integer'
                    elif type_val == icsqlalchemy.FLOAT_FIELD_TYPE:
                        col_type = u'sqlalchemy.Float'
                    elif type_val == icsqlalchemy.DATETIME_FIELD_TYPE:
                        col_type = u'sqlalchemy.DateTime'
                    elif type_val == icsqlalchemy.BIGINT_FIELD_TYPE:
                        col_type = u'sqlalchemy.BigInteger'
                    elif type_val == icsqlalchemy.BOOLEAN_FIELD_TYPE:
                        col_type = u'sqlalchemy.Boolean'
                    else:
                        col_type = u'sqlalchemy.%s' % type_val

                    column = u'sqlalchemy.Column(%s,  )' % (col_type, )
                elif obj_type == icsqlalchemy.LINK_TYPE:
                    # Это связь
                    column = u'sqlalchemy.ForeignKey(\'%s.id\')' % field_spc['table']
                else:
                    log.warning(u'Генерация модели. Не обрабатываемый тип <%s>' % obj_type)
                    continue

                line = u'\t%s = %s' % (field_name, column)
                field_lines.append(line)

            field_txt = u'\n'.join(field_lines)
            description = tab_spc.get('description', u'')
            class_txt = MODEL_CLASS_TXT_FMT % (model_name,
                                               manager_module_name,
                                               manager_name,
                                               description,
                                               tab_name,
                                               field_txt)
            module_txt = MODEL_MODULE_TXT_FMT % (description,
                                                 manager_module_name,
                                                 class_txt)

            if dst_module_filename is None:
                dst_module_filename = os.path.join(icmodel.getSchemeDir(),
                                                   '%s_model.py' % tab_name)
            return ic_extend.save_file_text(dst_module_filename, module_txt)
        except:
            log.fatal(u'Ошибка генерации модуля модели по ресурсу таблицы')
        return False

    def genModelManagerModuleByTabRes(self, tab_res_filename=None, dst_module_filename=None):
        """
        Генерация модуля менеджера модели по ресурсу таблицы.
        @param tab_res_filename: Полное имя файла ресурса таблицы.
        @param dst_module_filename: Полное имя результирующего файла модуля модели.
            Если не определено, то генерируется.
        @return: True/False.
        """
        try:
            tab_res = resfunc.LoadResource(tab_res_filename)
            tab_name = tab_res.keys()[0]
            tab_spc = tab_res[tab_name]
            manager_module_name = '%s_manager' % tab_name
            manager_name = 'ic%sModelManager' % ic_str.lower_symbols2_upper(tab_name)

            description = tab_spc.get('description', u'')
            module_txt = MODEL_MANAGER_TXT_FMT % (description,
                                                  manager_name,
                                                  description)

            if dst_module_filename is None:
                dst_module_filename = os.path.join(icmodel.getSchemeDir(),
                                                   '%s.py' % manager_module_name)
            return ic_extend.save_file_text(dst_module_filename, module_txt)
        except:
            log.fatal(u'Ошибка генерации модуля менеджера модели по ресурсу таблицы')
        return False
