#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NUMERIC


def py_lesser(val, cmp, *arg):
    return val < cmp


def py_lesser_or_equal(val, cmp, *arg):
    return val <= cmp


def py_great(val, cmp, *arg):
    return val > cmp


def py_great_or_equal(val, cmp, *arg):
    return val >= cmp


def py_between(val, cmp1, cmp2, *arg):
    return cmp1 <= val <= cmp2


def py_not_between(val, cmp1, cmp2, *arg):
    return not (cmp1 <= val <= cmp2)


# STRING
def py_equal(val, cmp, *arg):
    return val == cmp


def py_not_equal(val, cmp, *arg):
    return val != cmp


def py_contain(val, cmp, *arg):
    return cmp in val


def py_not_contain(val, cmp, *arg):
    return not (cmp in val)


def py_into(val, cmp, *arg):
    return val in cmp


def py_not_into(val, cmp, *arg):
    return not (val in cmp)


def py_left_equal(val, cmp, *arg):
    return val.startswith(cmp)


def py_right_equal(val, cmp, *arg):
    return val.endswith(cmp)


def py_mask(val, cmp, *arg):
    return True


def py_not_mask(val, cmp, *arg):
    return True


def py_is_null(val, cmp, *arg):
    return not bool(val)


def py_not_null(val, cmp, *arg):
    return bool(val)


# DATETIME
def py_datetime_equal(val, cmp, *arg):
    return val == cmp


def py_datetime_not_equal(val, cmp, *arg):
    return val != cmp


def py_datetime_into(val, cmp, *arg):
    return val in cmp


def py_datetime_not_into(val, cmp, *arg):
    return not (val in cmp)


def py_datetime_is_null(val, cmp, *arg):
    return val is None


def py_datetime_not_null(val, cmp, *arg):
    return val is not None


def py_datetime_lesser(val, cmp, *arg):
    return val < cmp


def py_datetime_lesser_or_equal(val, cmp, *arg):
    return val <= cmp


def py_datetime_great(val, cmp, *arg):
    return val > cmp


def py_datetime_great_or_equal(val, cmp, *arg):
    return val >= cmp


def py_datetime_between(val, cmp1, cmp2, *arg):
    return cmp1 <= val <= cmp2


def py_datetime_not_between(val, cmp1, cmp2, *arg):
    return not (cmp1 <= val <= cmp2)
