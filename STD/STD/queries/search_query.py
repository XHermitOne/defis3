#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from ic.db import icsqlalchemy
import sqlalchemy as sql_
from ic.utils import ic_time


class SearchManager(object):
    def __init__(self, manager=None):
        self.manager = manager
    
    def _date_query(self, tab, date_attr,  min, max, q=None, bConv=True):
        """
        Запрос по промежутку дат.
        @param tab: Таблица.
        @param date_attr: Атрибут поиска.
        @param min: Начальная дата.
        @param max: Конечная дата.
        @param q: Подготовленный запрос.
        """
        attr = getattr(tab.c, date_attr)
        date_min, date_max = None, None
        if min:
            if bConv:
                date_min = ic_time.strDateFmt2DateTime(min.strip(), '%Y.%m.%d')
            else:
                date_min = min
        if max:
            if bConv:
                date_max = ic_time.strDateFmt2DateTime(max.strip(), '%Y.%m.%d')
            else:
                date_max = max
        dq = None        
        if date_min and date_max:
            dq = attr.between(date_min, date_max)
        elif date_min:
            dq = (attr >= date_min)
        elif date_max:
            dq = (attr <= date_max)
        if q and dq:
            q &= dq
        elif dq:
            q = dq
        print(' *** date_query:', q, date_min, date_max)
        return q
    
    def get_search_query(self, search_dict):
        """
        Получить объект запроса по словарю выбранных параметров поиска.
        """
        db = self.manager.scheme
        tab = db.getTables()['registr']
        adds = db.getTables()['additional']
        doctab = db.getTables()['doccontent']
        doclinx = db.getTables()['doclinx']
        result = icsqlalchemy.char_length(tab.c.cod) == 21
        for param_name, param_val in search_dict.items():
            if param_name == 'name' and param_val:
                result &= tab.c.name.ilike('%%'+param_val+'%%')
            elif param_name == 'description' and param_val:
                result &= tab.c.description.ilike('%%'+param_val+'%%')
            elif param_name == 'num' and param_val:
                result &= tab.c.cod.ilike('%%'+param_val+'%%')
            elif param_name == 'num_min' and param_val and search_dict['num_max']:
                into = [('%05d' % i)[-5:] for i in range(int(param_val), int(search_dict['num_max']))]
                result &= icsqlalchemy.or_(*[tab.c.cod.endswith(i) for i in into])
            elif param_name == 'code' and param_val:
                result &= tab.c.cod.startswith(param_val)
            elif param_name == 'code_min' and param_val and search_dict['code_max']:
                result &= tab.c.cod.between(param_val, search_dict['code_max'])
            elif param_name == 'vid_doc' and param_val:
                result &= tab.c.vid_doc.like(param_val)
            elif param_name == 'sootvetstv' and param_val:
                result &= tab.c.jcard_status_low.like(param_val)
            elif param_name == 'status' and param_val:
                result &= tab.c.jcard_status.like(param_val)
            elif param_name == 'edit_date' and param_val:
                date_min, date_max = param_val
                qd = self._date_query(tab, 'cur_red', date_min, date_max, bConv=False)
                if qd:
                    result &= qd
            elif param_name == 'since_date' and param_val:
                date_min, date_max = param_val
                qd = self._date_query(tab, 'work_date', date_min, date_max)
                if qd:
                    result &= qd
            elif param_name == 'reg_date' and param_val:
                date_min, date_max = param_val
                qd = self._date_query(tab, 'enter_date', date_min, date_max)
                if qd:
                    result &= qd
            elif param_name == 'to_date' and param_val:
                date_min, date_max = param_val
                qd = self._date_query(tab, 'creation_date', date_min, date_max)
                if qd:
                    result &= qd
            # Нормативный / ненормативный
            elif param_name in 'typ_norm':
                norm, nonorm = '1', '0'
                if param_val[0] and param_val[1]:
                    result &= icsqlalchemy.or_(tab.c.jcard_type == norm,
                                               tab.c.jcard_type == nonorm)
                elif param_val[0]:
                    result &= tab.c.jcard_type == norm
                elif param_val[1]:
                    result &= tab.c.jcard_type == nonorm
            # Основной / изменяющий
            elif param_name == 'prz_typ':
                prz_osn, prz_change = '0', '1'
                if param_val[0] and param_val[1]:
                    result &= icsqlalchemy.or_(tab.c.typ_doc == prz_osn,
                                               tab.c.typ_doc == prz_change)
                elif param_val[0]:
                    result &= (tab.c.typ_doc == prz_osn)
                elif param_val[1]:
                    result &= (tab.c.typ_doc == prz_change)
            elif param_name == 'cls' and param_val:
                code_lst = [item[0] for item in param_val if item[1] == 1]
                if code_lst:
                    result &= icsqlalchemy.or_(*[tab.c.jcard_pravocls.ilike('%%'+code+'%%') for code in code_lst])

            elif param_name == 'dopvid' and param_val:
                dopvid, d1, d2 = param_val
                if dopvid or d1 or d2:
                    qd = self._date_query(adds, 'work_date', d1, d2)
                    # print ' *** dopvid:', dopvid
                    q = None
                    for item in dopvid:
                        cod_lst = item[-1]
                        if item[1] == 1 and len(cod_lst) > 0:
                            qc = (adds.c.vid_sved == cod_lst[0])
                            if len(cod_lst) > 1:
                                qc &= (adds.c.npa_state == cod_lst[1])
                            if len(cod_lst) > 2:
                                qc &= adds.c.source == item[0]
                                
                            if q:
                                q = icsqlalchemy.or_(q, qc)
                            else:
                                q = qc
                    q = icsqlalchemy.and_(q, qd) 
                    result &= tab.c.cod.in_(sql_.select([adds.c.cod], q))
            elif param_name == 'dop_title' and param_val:
                result &= tab.c.name.ilike('%%'+param_val+'%%')
            elif param_name == 'dop_descr' and param_val:
                result &= tab.c.description.ilike('%%'+param_val+'%%')
            elif param_name == 'dop_text' and param_val:
                pass
            elif param_name == 'body' and param_val:
                q = doclinx.c.doc_txt.ilike('%%'+param_val+'%%')
                result &= tab.c.cod.in_(sql_.select([doclinx.c.doc_cod], q))
            elif param_name == 'dop_date_min':
                pass
            elif param_name == 'org' and param_val:
                code_lst = [item[0] for item in param_val if item[1] == 1]
                # print ' *** code_lst:', code_lst
                if code_lst:
                    result &= icsqlalchemy.or_(*[tab.c.org_prin.ilike('%%'+code+'%%') for code in code_lst])
            else:
                print('Unknow param:', param_name, param_val)

        return result
