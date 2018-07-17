#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции работы с электронной почтой.
"""

import os
import os.path
import email
import smtplib

from ic.log import log

__version__ = (0, 0, 1, 1)

EMAIL_ADR_DELIMETER = u';'
DEFAULT_ENCODING = 'utf-8'

# Защита соединения
SMTP_PROTECT_NO = u'NO'                 # Нет
SMTP_PROTECT_STARTTLS = u'STARTTLS'     # STARTTLS
SMTP_PROTECT_SSL_TLS = u'SSL/TLS'       # SSL/TLS

# Метод аутентификации
SMTP_AUTHENT_NO = u'NO'                     # Без аутентификации
SMTP_AUTHENT_UNDEFENDED = u'UNDEFENDED'     # Обычный пароль
SMTP_AUTHENT_ENCRYPTED = u'ENCRYPTED'       # Зашифрованный пароль
SMTP_AUTHENT_KERBEROS = u'Kerberos/GSSAPI'  # Kerberos/GSSAPI
SMTP_AUTHENT_NTLM = u'NTLM'                 # NTLM
SMTP_AUTHENT_OAUTH2 = u'OAuth2'             # OAuth2


class icEMailSender(object):
    """
    Отправщик писем.
    """

    def __init__(self, from_adr=None, to_adr=None,
                 subject=None, body=None, attache_files=None,
                 smtp_server=None, smtp_port=None,
                 login=None, password=None, enable_send=True,
                 encoding='utf-8',
                 outbox_dir=None, auto_del_files=False,
                 prev_send_cmd=None, post_send_cmd=None,
                 connect_protect=None, authent=None):
        """
        Конструктор.
        @param from_adr: Адрес отправителя.
        @param to_adr: Адрес/адреса получаетелей.
            Может задаваться списком или текстом разделенным EMAIL_ADR_DELIMETER.
        @param subject: Заголовок письма.
        @param body: Тело письма,
        @param attache_files: Список прикрепляемых файлов.
        @param smtp_server: Адрес SMTP сервера.
        @param smtp_port: Порт SMTP сервера. Обычно по умолчанию 25.
        @param login: Логин пользователя SMTP сервера.
        @param password: Пароль пользователя SMTP сервера.
        @param enable_send: Вкл./выкл. отправки писем.
        @param encoding: Кодировка писем. По умолчанию UTF-8.
        @param outbox_dir: Папка исходящих файлов.
        @param auto_del_files: Автоматически удалять прикрепляемые файлы после отправки?
        @param prev_send_cmd: Комманда, выполняемая перед отправкой письма.
        @param post_send_cmd: Комманда, выполняемая после отправки письма.
        @param connect_protect: Защита соединения.
        @param authent: Метод аутентификации.
        """
        self.from_adr = from_adr
        self.to_adr = to_adr.split(EMAIL_ADR_DELIMETER) if type(to_adr) in (str, unicode) else to_adr
        self.subject = subject
        self.body = body
        self.attache_files = attache_files
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.login = login
        self.password = password

        self.enable_send = enable_send
        self.encoding = encoding
        self.outbox_dir = outbox_dir
        self.auto_del_files = auto_del_files

        self.prev_send_cmd = prev_send_cmd
        self.post_send_cmd = post_send_cmd

        # Защита соединения
        self.connect_protect = connect_protect
        # Метод аутентификации
        self.authent = authent

    def _encode(self, txt, from_codepage, to_codepage):
        """
        Перекодировка строки из одной кодовой страницы в другую.
        """
        if isinstance(txt, str):
            return unicode(txt, from_codepage).encode(to_codepage)
        elif isinstance(txt, unicode):
            return txt.encode(to_codepage)

    def _do_cmd_list(self, cmd_list, mode=os.P_WAIT):
        """
        Выполнение списка комманд ОС.
        @param cmd_list: Список команд ОС.
        """
        if cmd_list and isinstance(cmd_list, list):
            for cmd in cmd_list:
                cmd = cmd.strip()
                if cmd:
                    self._do_cmd(cmd, mode)

    def _parse_cmd(self, cmd):
        """
        Распарсить Коммандную строку.
        """
        cmd_arg = cmd.split(' ')
        return tuple(cmd_arg)

    def _do_cmd(self, cmd, mode=None):
        """
        Выполнить команду в указанном режиме (с ожиданием завершения/без ожидания).
        """
        try:
            if mode is None:
                os.system(cmd)
            else:
                arg_cmd = self._parse_cmd(cmd)
                os.spawnl(mode, arg_cmd[0], *arg_cmd)

            log.info(u'Команда ОС <%s> выполнена' % cmd)
        except:
            log.fatal(u'Ошибка выполнения коммманды ОС: %s' % cmd)

    def send_mail(self, from_adr=None, to_adr=None,
                  subject=None, body=None, attache_files=None,
                  smtp_server=None, smtp_port=None,
                  login=None, password=None,
                  connect_protect=None, authent=None):
        """
        Функция отправки  письма. Если какой  параметр функции
            None, то этот параметр берется из внутренних настроек отправщика.
        @param from_adr: Адрес отправителя.
        @param to_adr: Адрес/адреса получаетелей.
            Может задаваться списком или текстом разделенным EMAIL_ADR_DELIMETER.
        @param subject: Заголовок письма.
        @param body: Тело письма,
        @param attache_files: Список прикрепляемых файлов.
        @param smtp_server: Адрес SMTP сервера.
        @param smtp_port: Порт SMTP сервера. Обычно по умолчанию 25.
        @param login: Логин пользователя SMTP сервера.
        @param password: Пароль пользователя SMTP сервера.
        @return: True/False.
        """
        if self.prev_send_cmd:
            self._do_cmd_list(self.prev_send_cmd, None)

        try:
            result = self._send_mail(from_adr, to_adr,
                                     subject, body, attache_files,
                                     smtp_server, smtp_port,
                                     login, password,
                                     connect_protect, authent)
        except:
            log.fatal(u'Ошибка отправки письма')
            result = False

        if self.post_send_cmd:
            self._do_cmd_list(self.post_send_cmd)

        return result

    def _send_mail(self, from_adr=None, to_adr=None,
                   subject=None, body=None, attache_files=None,
                   smtp_server=None, smtp_port=None,
                   login=None, password=None,
                   connect_protect=None, authent=None):
        """
        Функция отправки  письма. Если какой  параметр функции
            None, то этот параметр берется из внутренних настроек отправщика.
        @param from_adr: Адрес отправителя.
        @param to_adr: Адрес/адреса получаетелей.
            Может задаваться списком или текстом разделенным EMAIL_ADR_DELIMETER.
        @param subject: Заголовок письма.
        @param body: Тело письма,
        @param attache_files: Список прикрепляемых файлов.
        @param smtp_server: Адрес SMTP сервера.
        @param smtp_port: Порт SMTP сервера. Обычно по умолчанию 25.
        @param login: Логин пользователя SMTP сервера.
        @param password: Пароль пользователя SMTP сервера.
        @return: True/False.
        """
        # Отправка писем выключена
        if not self.enable_send:
            log.warning(u'Отправка писем выключена')
            return False

        # Проверка входых параметров
        from_adr = self.from_adr if from_adr is None else from_adr
        to_adr = self.to_adr if to_adr is None else to_adr
        subject = self.subject if subject is None else subject
        body = self.body if body is None else body
        attache_files = self.attache_files if attache_files is None else attache_files
        smtp_server = self.smtp_server if smtp_server is None else smtp_server
        smtp_port = self.smtp_port if smtp_port is None else smtp_port
        login = self.login if login is None else login
        password = self.password if password is None else password
        connect_protect = self.connect_protect if connect_protect is None else connect_protect
        authent = self.authent if authent is None else authent

        # Проверка типов входных аргументов
        assert type(from_adr) in (str, unicode)
        assert type(to_adr) in (list, tuple)
        assert type(attache_files) in (list, tuple)

        # Создать сообщение
        msg = email.MIMEMultipart.MIMEMultipart()

        msg['From'] = self._encode(from_adr, DEFAULT_ENCODING, self.encoding)
        msg['To'] = self._encode(email.Utils.COMMASPACE.join(to_adr), DEFAULT_ENCODING, self.encoding)
        msg['Date'] = email.Utils.formatdate(localtime=True)
        msg['Subject'] = self._encode(subject, DEFAULT_ENCODING, self.encoding)
        msg.attach(email.MIMEText.MIMEText(self._encode(body, DEFAULT_ENCODING, self.encoding)))

        # Если файлы не определены, то посмотреть в папке исходящих файлов
        if not attache_files and self.outbox_dir:
            attache_files = self.get_outbox_filenames()

        # Прикрепление файлов
        for filename in attache_files:
            part = email.MIMEBase.MIMEBase('application', 'octet-stream')
            part.set_payload(open(filename, 'rb').read())
            email.Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(filename))
            msg.attach(part)

            file_size = os.stat(filename).st_size
            log.info(u'Файл <%s> (%s) прикреплен к письму' % (filename, file_size))

        msg_txt = msg.as_string()

        # Соединение с SMTP сервером и отправка сообщения
        try:
            smtp = smtplib.SMTP(smtp_server, smtp_port)
            smtp.set_debuglevel(0)
            if connect_protect == SMTP_PROTECT_STARTTLS:
                # ВНИМАНИЕ! Если используем защиту связи STARTTLS, то необходимо
                # перевести сервер в режим с помощью метода .starttls()
                smtp.starttls()

            if login and authent != SMTP_AUTHENT_NO:
                log.info(u'SMTP. %s. login: <%s> password: <%s>' % (authent, login, password))
                smtp.login(login, password)

            to_adr = [to.strip() for to in to_adr]
            log.info(u'Отправка письма с адреса <%s> на адрес <%s>' % (from_adr, to_adr))
            # log.debug(msg_txt)
            smtp.sendmail(from_adr, to_adr, msg_txt)
            smtp.close()

            log.info(u'Письмо от %s к %s отправленно' % (from_adr, to_adr))

        except smtplib.SMTPException:
            log.fatal(u'SMTP. Ошибка отправки письма')
            return False

        if attache_files and self.auto_del_files:
            # Удалить прикрепляемые файлы?
            for file_name in attache_files:
                if os.path.exists(file_name):
                    try:
                        os.remove(file_name)
                        log.info(u'Файл <%s> удален' % file_name)
                    except:
                        log.fatal(u'Ошибка удаления файла <%s>' % file_name)
                        return False
        return True

    def get_outbox_filenames(self, outbox_dir=None):
        """
        Посмотреть есть ли файлы в папке исходящих файлов.
        @param outbox_dir: Папка исходящих файлов.
        @return: Список файлов находящихся в папке исходящих файлов.
        """
        outbox_dir = self.outbox_dir if outbox_dir is None else outbox_dir

        outbox_filenames = list()
        if outbox_dir:
            if os.path.isdir(outbox_dir):
                outbox_filenames = [os.path.join(outbox_dir, element) for element in os.listdir(outbox_dir) if
                                    os.path.isfile(os.path.join(outbox_dir, element))]
        return outbox_filenames


def send_mail(*args, **kwargs):
    """
    Отсылка письма из коммандной строки.
    """
    mail_sender = icEMailSender(*args, **kwargs)
    result = mail_sender.send_mail()
    return result


