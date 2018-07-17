#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Схемы размещения по умолчанию.
"""

try:
    from . import board
except ValueError:
    import board

from ic.log import log
from ic.utils import ic_str

DEFAULT_X_OFFSET = 0
DEFAULT_Y_OFFSET = 0

MAX_Y_OFFSET = 1


def init_cell_points(positions, x_offset=DEFAULT_X_OFFSET, y_offset=DEFAULT_Y_OFFSET,
                     cell_width=board.DEFAULT_CELL_WIDTH, cell_height=board.DEFAULT_CELL_HEIGHT):
    """
    Заполнение списка точек расположения ячеек
    по списку позиций.
    @param positions: Список позиций.
    @param x_offset: Точка смещения. Координата X.
    @param y_offset: Точка смещения. Координата Y.
    @param cell_width: Размер ячейки в точках. Ширина.
    @param cell_height: Размер ячейки в точках. Высота.
    @return: Заполненный список точек.
    """
    points = list()
    for i, pos in enumerate(positions):
        try:
            x = pos[0]
            y = pos[1]
            point = dict(left=x_offset + x * cell_width,
                         top=y_offset + (MAX_Y_OFFSET - y) * cell_height,
                         idx=i)
            points.append(point)
        except:
            log.fatal(u'Ошибка определения позиции <%s> расположения ячейки' % pos)
    return points


def _gen_pseudograph_line(line, pseudograph_symb, i):
    """
    Генерация линии. Установка символа псевдографики в строку методом наложения
    @param line: Обрабатываемая строка.
    @param pseudograph_symb: Вставляемый в строку символ псевдографики.
    @param i: Номер символа в строке.
    @return: Измененная строка.
    """
    prev_symb = line[i]
    result_symb = ic_str.overlayPseudoGraph(pseudograph_symb, prev_symb,
                                            default_symb=pseudograph_symb)
    # log.debug(u'%d. Слияние символов <%s> + <%s> = <%s>' % (i, pseudograph_symb, prev_symb, result_symb))
    return line[:i]+result_symb+line[i+1:]


def gen_layout_scheme_txt(positions):
    """
    Генерация текста схемы размещения в виде псевдографики.
    @param positions: Список позиций.
    @return: Текст схемы размещения.  
        Например:
           ┌──┐  ┌──┐  ┌──┬──┐  ┌──┐  ┌──┐  ┌──┬──┐
        ┌──┤ 3├──┤ 6├──┤ 9│11├──┤14├──┤17├──┤20│22│
        │ 1├──┤ 4├──┤ 7├──┼──┤12├──┤15├──┤18├──┼──┤
        └──┤ 2├──┤ 5├──┤ 8│10├──┤13├──┤16├──┤19│21│
           └──┘  └──┘  └──┴──┘  └──┘  └──┘  └──┴──┘     
    """
    max_x = max([pos[0] for pos in positions])
    max_coord_x = (max_x + 1) * 3 + 1
    lines = [u' ' * max_coord_x, u' ' * max_coord_x, u' ' * max_coord_x,
             u' ' * max_coord_x, u' ' * max_coord_x]
    for i, pos in enumerate(positions):
        try:
            x = pos[0]
            y = pos[1]

            line_0 = 2 - int(y * 2)
            line_1 = line_0 + 1
            line_2 = line_0 + 2

            col_start = x * 3
            col_stop = col_start + 4

            for i_col in range(col_start, col_stop):
                # log.debug(u'Колонка: %s' % i_col)
                if i_col == col_start:
                    lines[line_0] = _gen_pseudograph_line(lines[line_0], ic_str.PSEUDOGRAPH[2], i_col)    # ┌
                    lines[line_1] = _gen_pseudograph_line(lines[line_1], ic_str.PSEUDOGRAPH[0], i_col)    # │
                    lines[line_2] = _gen_pseudograph_line(lines[line_2], ic_str.PSEUDOGRAPH[4], i_col)    # └
                elif i_col == (col_stop-1):
                    lines[line_0] = _gen_pseudograph_line(lines[line_0], ic_str.PSEUDOGRAPH[3], i_col)    # ┐
                    lines[line_1] = _gen_pseudograph_line(lines[line_1], ic_str.PSEUDOGRAPH[0], i_col)    # │
                    lines[line_2] = _gen_pseudograph_line(lines[line_2], ic_str.PSEUDOGRAPH[5], i_col)    # ┘
                elif i_col == (col_start+1):
                    n = (u' ' + str(i + 1)) if len(str(i + 1)) == 1 else str(i + 1)
                    lines[line_1] = lines[line_1][:i_col] + n + lines[line_1][i_col + 2:]
                    lines[line_0] = _gen_pseudograph_line(lines[line_0], ic_str.PSEUDOGRAPH[1], i_col)    # ─
                    lines[line_2] = _gen_pseudograph_line(lines[line_2], ic_str.PSEUDOGRAPH[1], i_col)    # ─
                else:
                    lines[line_0] = _gen_pseudograph_line(lines[line_0], ic_str.PSEUDOGRAPH[1], i_col)    # ─
                    lines[line_2] = _gen_pseudograph_line(lines[line_2], ic_str.PSEUDOGRAPH[1], i_col)    # ─
        except:
            log.fatal(u'Ошибка определения позиции %s расположения ячейки' % str(pos))

    txt = u'\n'.join(lines)
    return txt


DEFAULT_WINTER_1_AXLE_LABEL = u'1-осный тягач. Вариант загрузки <ЗИМА>. 22 палета'
DEFAULT_WINTER_1_AXLE_POS = [(0, 0), (0, 1),
                             (1, 0), (1, 1),
                             (2, 0), (2, 1),
                             (3, 0), (3, 1),
                             (4, 0), (4, 1),
                             (5, 0), (5, 1),
                             (6, 0.5),
                             (7, 0), (7, 1),
                             (8, 0), (8, 1),
                             (9, 0.5),
                             (10, 0), (10, 1),
                             (11, 0), (11, 1),
                             ]
DEFAULT_WINTER_1_AXLE = init_cell_points(DEFAULT_WINTER_1_AXLE_POS)
DEFAULT_WINTER_1_AXLE_SCHEME = gen_layout_scheme_txt(DEFAULT_WINTER_1_AXLE_POS)

DEFAULT_SUMMER_1_AXLE_LABEL = u'1-осный тягач. Вариант загрузки <ЛЕТО>. 22 палета'
DEFAULT_SUMMER_1_AXLE_POS = [(0, 0), (0, 1),
                             (1, 0), (1, 1),
                             (2, 0), (2, 1),
                             (3, 0), (3, 1),
                             (4, 0), (4, 1),
                             (5, 0), (5, 1),
                             (6, 0.5),
                             (7, 0), (7, 1),
                             (8, 0.5),
                             (9, 0), (9, 1),
                             (10, 0.5),
                             (11, 0), (11, 1),
                             (12, 0.5),
                             ]
DEFAULT_SUMMER_1_AXLE = init_cell_points(DEFAULT_SUMMER_1_AXLE_POS)
DEFAULT_SUMMER_1_AXLE_SCHEME = gen_layout_scheme_txt(DEFAULT_SUMMER_1_AXLE_POS)

DEFAULT_22_PALET_2_AXLE_LABEL = u'2-осный тягач. 22 палета'
DEFAULT_22_PALET_2_AXLE_POS = [(0, 0), (0, 1),
                               (1, 0), (1, 1),
                               (2, 0.5),
                               (3, 0), (3, 1),
                               (4, 0.5),
                               (5, 0), (5, 1),
                               (6, 0), (6, 1),
                               (7, 0), (7, 1),
                               (8, 0.5),
                               (9, 0), (9, 1),
                               (10, 0.5),
                               (11, 0), (11, 1),
                               (12, 0), (12, 1),
                               ]
DEFAULT_WINTER_2_AXLE = init_cell_points(DEFAULT_22_PALET_2_AXLE_POS)
DEFAULT_22_PALET_2_AXLE_SCHEME = gen_layout_scheme_txt(DEFAULT_22_PALET_2_AXLE_POS)

DEFAULT_20_PALLET_2_AXLE_LABEL = u'2-осный тягач. 20 палет'
DEFAULT_20_PALLET_2_AXLE_POS = [(0, 0), (0, 1),
                                (1, 0.5),
                                (2, 0.5),
                                (3, 0), (3, 1),
                                (4, 0.5),
                                (5, 0), (5, 1),
                                (6, 0), (6, 1),
                                (7, 0), (7, 1),
                                (8, 0.5),
                                (9, 0), (9, 1),
                                (10, 0.5),
                                (11, 0), (11, 1),
                                (12, 0.5),
                                ]
DEFAULT_20_PALLET_2_AXLE = init_cell_points(DEFAULT_20_PALLET_2_AXLE_POS)
DEFAULT_20_PALLET_2_AXLE_SCHEME = gen_layout_scheme_txt(DEFAULT_20_PALLET_2_AXLE_POS)

DEFAULT_19_PALLET_LABEL = u'19 - местная схема погрузки'
DEFAULT_19_PALLET_POS = [(0, 0.5),
                         (1, 0),  (1, 1),
                         (2, 0.5),
                         (3, 0), (3, 1),
                         (4, 0.5),
                         (5, 0), (5, 1),
                         (6, 0.5),
                         (7, 0), (7, 1),
                         (8, 0.5),
                         (9, 0), (9, 1),
                         (10, 0.5),
                         (11, 0), (11, 1),
                         (12, 0.5),
                         ]
DEFAULT_19_PALLET = init_cell_points(DEFAULT_19_PALLET_POS)
DEFAULT_19_PALLET_SCHEME = gen_layout_scheme_txt(DEFAULT_19_PALLET_POS)

DEFAULT_20_PALLET_LABEL = u'20 - местная схема погрузки'
DEFAULT_20_PALLET_POS = [(0, 0.5),
                         (1, 0),  (1, 1),
                         (2, 0.5),
                         (3, 0), (3, 1),
                         (4, 0.5),
                         (5, 0), (5, 1),
                         (6, 0.5),
                         (7, 0), (7, 1),
                         (8, 0), (8, 1),
                         (9, 0.5),
                         (10, 0), (10, 1),
                         (11, 0.5),
                         (12, 0), (12, 1),
                         ]
DEFAULT_20_PALLET = init_cell_points(DEFAULT_20_PALLET_POS)
DEFAULT_20_PALLET_SCHEME = gen_layout_scheme_txt(DEFAULT_20_PALLET_POS)

DEFAULT_21_PALLET_LABEL = u'21 - местная схема погрузки'
DEFAULT_21_PALLET_POS = [(0, 0.5),
                         (1, 0),  (1, 1),
                         (2, 0.5),
                         (3, 0), (3, 1),
                         (4, 0.5),
                         (5, 0), (5, 1),
                         (6, 0.5),
                         (7, 0), (7, 1),
                         (8, 0), (8, 1),
                         (9, 0), (9, 1),
                         (10, 0), (10, 1),
                         (11, 0.5),
                         (12, 0), (12, 1),
                         ]
DEFAULT_21_PALLET = init_cell_points(DEFAULT_21_PALLET_POS)
DEFAULT_21_PALLET_SCHEME = gen_layout_scheme_txt(DEFAULT_21_PALLET_POS)

DEFAULT_22_PALLET_LABEL = u'22 - местная схема погрузки'
DEFAULT_22_PALLET_POS = [(0, 0.5),
                         (1, 0),  (1, 1),
                         (2, 0.5),
                         (3, 0), (3, 1),
                         (4, 0.5),
                         (5, 0), (5, 1),
                         (6, 0), (6, 1),
                         (7, 0), (7, 1),
                         (8, 0), (8, 1),
                         (9, 0), (9, 1),
                         (10, 0), (10, 1),
                         (11, 0.5),
                         (12, 0), (12, 1),
                         ]
DEFAULT_22_PALLET = init_cell_points(DEFAULT_22_PALLET_POS)
DEFAULT_22_PALLET_SCHEME = gen_layout_scheme_txt(DEFAULT_22_PALLET_POS)

DEFAULT_23_PALLET_LABEL = u'23 - местная схема погрузки'
DEFAULT_23_PALLET_POS = [(0, 0.5),
                         (1, 0),  (1, 1),
                         (2, 0.5),
                         (3, 0), (3, 1),
                         (4, 0), (4, 1),
                         (5, 0), (5, 1),
                         (6, 0), (6, 1),
                         (7, 0), (7, 1),
                         (8, 0), (8, 1),
                         (9, 0), (9, 1),
                         (10, 0), (10, 1),
                         (11, 0.5),
                         (12, 0), (12, 1),
                         ]
DEFAULT_23_PALLET = init_cell_points(DEFAULT_23_PALLET_POS)
DEFAULT_23_PALLET_SCHEME = gen_layout_scheme_txt(DEFAULT_23_PALLET_POS)

DEFAULT_24_PALLET_LABEL = u'24 - местная схема погрузки'
DEFAULT_24_PALLET_POS = [(0, 0.5),
                         (1, 0),  (1, 1),
                         (2, 0.5),
                         (3, 0), (3, 1),
                         (4, 0), (4, 1),
                         (5, 0), (5, 1),
                         (6, 0), (6, 1),
                         (7, 0), (7, 1),
                         (8, 0), (8, 1),
                         (9, 0), (9, 1),
                         (10, 0), (10, 1),
                         (11, 0), (11, 1),
                         (12, 0), (12, 1),
                         ]
DEFAULT_24_PALLET = init_cell_points(DEFAULT_24_PALLET_POS)
DEFAULT_24_PALLET_SCHEME = gen_layout_scheme_txt(DEFAULT_24_PALLET_POS)


DEFAULT_19_PALLET_BACK1_LABEL = u'19 - местная схема погрузки. Расположение 12 позиций. Нагрузка на задние оси'
DEFAULT_19_PALLET_BACK1_POS = [(0, 0.5),
                               (1, 0),  (1, 1),
                               (2, 0.5),
                               (3, 0), (3, 1),
                               (4, 0.5),
                               (5, 0), (5, 1),
                               (6, 0.5),
                               (7, 0), (7, 1),
                               (8, 0.5),
                               (9, 0), (9, 1),
                               (10, 0), (10, 1),
                               (11, 0), (11, 1),
                               ]
DEFAULT_19_PALLET_BACK1 = init_cell_points(DEFAULT_19_PALLET_BACK1_POS)
DEFAULT_19_PALLET_BACK1_SCHEME = gen_layout_scheme_txt(DEFAULT_19_PALLET_BACK1_POS)


DEFAULT_20_PALLET_MID1_LABEL = u'20 - местная схема погрузки. Расположение 13 позиций. Нагрузка на середину'
DEFAULT_20_PALLET_MID1_POS = [(0, 0.5),
                              (1, 0),  (1, 1),
                              (2, 0.5),
                              (3, 0), (3, 1),
                              (4, 0.5),
                              (5, 0), (5, 1),
                              (6, 0), (6, 1),
                              (7, 0.5),
                              (8, 0), (8, 1),
                              (9, 0.5),
                              (10, 0), (10, 1),
                              (11, 0.5),
                              (12, 0), (12, 1),
                              ]
DEFAULT_20_PALLET_MID1 = init_cell_points(DEFAULT_20_PALLET_MID1_POS)
DEFAULT_20_PALLET_MID1_SCHEME = gen_layout_scheme_txt(DEFAULT_20_PALLET_MID1_POS)

DEFAULT_20_PALLET_MID2_LABEL = u'20 - местная схема погрузки. Расположение 13 позиций. Нагрузка на ось1 прицепа'
DEFAULT_20_PALLET_MID2_POS = [(0, 0.5),
                              (1, 0),  (1, 1),
                              (2, 0.5),
                              (3, 0), (3, 1),
                              (4, 0.5),
                              (5, 0), (5, 1),
                              (6, 0.5),
                              (7, 0), (7, 1),
                              (8, 0), (8, 1),
                              (9, 0.5),
                              (10, 0), (10, 1),
                              (11, 0.5),
                              (12, 0), (12, 1),
                              ]
DEFAULT_20_PALLET_MID2 = init_cell_points(DEFAULT_20_PALLET_MID2_POS)
DEFAULT_20_PALLET_MID2_SCHEME = gen_layout_scheme_txt(DEFAULT_20_PALLET_MID2_POS)

# Схемы используемый по умолчанию
DEFAULT_USE_LAYOUT_SCHEME_POS = (DEFAULT_19_PALLET_POS,
                                 DEFAULT_20_PALLET_POS,
                                 DEFAULT_21_PALLET_POS,
                                 DEFAULT_22_PALLET_POS,
                                 DEFAULT_23_PALLET_POS,
                                 DEFAULT_24_PALLET_POS,
                                 DEFAULT_19_PALLET_BACK1_POS,
                                 DEFAULT_20_PALLET_MID1_POS,
                                 DEFAULT_20_PALLET_MID2_POS,
                                 )

DEFAULT_USE_LAYOUT_SCHEME_POINT = (DEFAULT_19_PALLET,
                                   DEFAULT_20_PALLET,
                                   DEFAULT_21_PALLET,
                                   DEFAULT_22_PALLET,
                                   DEFAULT_23_PALLET,
                                   DEFAULT_24_PALLET,
                                   DEFAULT_19_PALLET_BACK1,
                                   DEFAULT_20_PALLET_MID1,
                                   DEFAULT_20_PALLET_MID2,
                                   )

DEFAULT_USE_LAYOUT_SCHEME = (dict(label=DEFAULT_19_PALLET_LABEL,
                                  pos=DEFAULT_19_PALLET_POS,
                                  point=DEFAULT_19_PALLET,
                                  txt=DEFAULT_19_PALLET_SCHEME),
                             dict(label=DEFAULT_20_PALLET_LABEL,
                                  pos=DEFAULT_20_PALLET_POS,
                                  point=DEFAULT_20_PALLET,
                                  txt=DEFAULT_20_PALLET_SCHEME),
                             dict(label=DEFAULT_21_PALLET_LABEL,
                                  pos=DEFAULT_21_PALLET_POS,
                                  point=DEFAULT_21_PALLET,
                                  txt=DEFAULT_21_PALLET_SCHEME),
                             dict(label=DEFAULT_22_PALLET_LABEL,
                                  pos=DEFAULT_22_PALLET_POS,
                                  point=DEFAULT_22_PALLET,
                                  txt=DEFAULT_22_PALLET_SCHEME),
                             dict(label=DEFAULT_23_PALLET_LABEL,
                                  pos=DEFAULT_23_PALLET_POS,
                                  point=DEFAULT_23_PALLET,
                                  txt=DEFAULT_23_PALLET_SCHEME),
                             dict(label=DEFAULT_24_PALLET_LABEL,
                                  pos=DEFAULT_24_PALLET_POS,
                                  point=DEFAULT_24_PALLET,
                                  txt=DEFAULT_24_PALLET_SCHEME),
                             dict(label=DEFAULT_19_PALLET_BACK1_LABEL,
                                  pos=DEFAULT_19_PALLET_BACK1_POS,
                                  point=DEFAULT_19_PALLET_BACK1,
                                  txt=DEFAULT_19_PALLET_BACK1_SCHEME),
                             dict(label=DEFAULT_20_PALLET_MID1_LABEL,
                                  pos=DEFAULT_20_PALLET_MID1_POS,
                                  point=DEFAULT_20_PALLET_MID1,
                                  txt=DEFAULT_20_PALLET_MID1_SCHEME),
                             dict(label=DEFAULT_20_PALLET_MID2_LABEL,
                                  pos=DEFAULT_20_PALLET_MID2_POS,
                                  point=DEFAULT_20_PALLET_MID2,
                                  txt=DEFAULT_20_PALLET_MID2_SCHEME),
                             )


def test():
    """
    Функция тестирования.
    """
    from ic import config

    log.init(config)

    txt = gen_layout_scheme_txt(DEFAULT_WINTER_1_AXLE_POS)
    print(txt)

if __name__ == '__main__':
    test()
