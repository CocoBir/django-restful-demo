# -*- coding: utf-8 -*-

"""

    define customer exception
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    specific customer exception

    :Created: 2016-8-4
    :Copyright: (c) 2016<smileboywtu@gmail.com>

"""

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class Status(object):
    """customer status code"""

    # 状态信息
    success = 'ok'
    failure = 'error'

    # 状态码
    code = {
        'ok': 0,                    # 成功返回
        'err': -1,                  # 标准错误
        'unknown': 1,               # 位置错误
        'params_type_err': 72201,   # 参数类型错误
        'params_less_err': 72202,   # 参数缺失

        'db_field_err': 72203,      # 参数长度不符合要求
        'db_integrity_err': 72204,  # 破坏数据的完整性
        'db_nexist_err': 72205,     # 指定对象不存在

        'db_referenced_err': 72206, # 数据库有依赖，禁止删除
        'index_err': 72207          # 请求的offset超出最大数据里量
    }


class OffsetOutOfRangeException(Exception):
    """index out of range"""
    def __init__(self):
        self.code = Status.code['index_err']
        self.message = 'index value is out of range'


class ParamNotEnoughException(Exception):
    """field not exist"""
    def __init__(self, name):
        self.code = Status.code['params_less_err']
        self.message = {name: 'need params.'}


class ParamTypeException(Exception):
    """field type error"""
    def __init__(self, name):
        self.code = Status.code['params_type_err']
        self.message = {name: 'type error.'}


class DBFieldLengthException(Exception):
    """field length exception"""
    def __init__(self, name):
        self.code = Status.code['db_field_err']
        self.message = {name: "field is too long."}


class DBRelyOnException(Exception):
    """entry be relied by others"""
    def __init__(self, name):
        self.code = Status.code['db_referenced_err']
        self.message = {name: 'entry relied by others, delete operation not allowed.'}


class DBIntegrityException(Exception):
    """entry be relied by others"""
    def __init__(self, name):
        self.code = Status.code['db_integrity_err']
        self.message = {name: 'entry name is already in use, choose another.'}


class ObjectNotExistException(Exception):
    """entry do not exist"""
    def __init__(self, pk):
        self.code = Status.code['db_nexist_err']
        self.message = {pk: 'entry not exist.'}
