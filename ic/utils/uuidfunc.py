#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import hashlib

__version__ = (0, 1, 1, 2)


def get_uuid(*args):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    return str(uuid.uuid4())


def get_uuid_attr(uuid_str, *attrs):
    """
    Переобразовать UUID в уникальное имя атрибута.

    :param uuid_str: UUID в строковом представлении.
    :param attrs: Список дополнительных атрибутов.
    :return: Сгенерированная строка.
    """
    uuid_str = uuid_str.replace('-', '_')
    for attr in attrs:
        uuid_str += '_'+str(attr)
    return uuid_str


def get_passport_check_sum(passport, asUUID=True):
    """
    Получить контрольную сумму паспорта.

    :param passport: Паспорт.
    :param asUUID: Преобразовать к UUID
        (XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX) виду?
    :return: Строка контрольной суммы.
    """
    data = str(passport)
    encode_data = data.encode()
    data = hashlib.md5(encode_data).hexdigest()
    if asUUID:
        data = data[:8]+'-'+data[8:12]+'-'+data[12:16]+'-'+data[16:20]+'-'+data[20:]
    return data


def valid_uuid(UUID):
    """
    Проверка корректного значения UUID.

    :return: True/False.
    """
    if not isinstance(UUID, str):
        UUID = str(UUID)
    return len(UUID) == 36 and UUID[8] == '-' and UUID[13] == '-' and UUID[18] == '-' and UUID[23] == '-'


def test():
    """
    Тестирование.
    """
    psp = (('A', 'a', None, 'test', 'STD'),)
    print(get_passport_check_sum(psp))


if __name__ == '__main__':
    test()
