#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Класс системного менеджера моделей на основе SQLAlchemy.
"""

import sqlalchemy
import sqlalchemy.orm

from ic.log import log

__version__ = (0, 1, 1, 1)


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

