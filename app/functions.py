# -*- coding: utf-8 -*-

import datetime
import importlib
import pkgutil
import random
import string
from decimal import Decimal
from functools import wraps
from inspect import getmembers, isfunction

from flask import  g, redirect, request, session, url_for as origin_url_for

from app.extensions import db


def url_for(endpoint, **values):
    endpoint_array = endpoint.split(".")
    if len(endpoint_array) > 2:
        endpoint = "%s.%s" % ("_".join(endpoint_array[:-1]), endpoint_array[-1])
    return origin_url_for(endpoint, **values)


def get_sub_modules(module_name):
    """获取子模块迭代器"""

    package = importlib.import_module(module_name)
    for module in pkgutil.iter_modules(package.__path__):
        yield importlib.import_module("%s.%s" % (module_name, module[1]))


def get_module_functions(module_name):
    """获取模块下所有函数的迭代器"""

    module = importlib.import_module(module_name)
    for member in getmembers(module, isfunction):
        yield member


def get_endpoint():
    """获取当前的endpoint"""

    return request.endpoint.replace("_", ".")


def login_required(admin=True):
    """登录认证装饰器"""

    def _login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.services import user_srv

            if "user_id" not in session:
                return redirect(url_for("auth.login", next=get_endpoint()))

            user = user_srv.get(session["user_id"])
            if not user:
                session.clear()
                return redirect(url_for("auth.login"))

            g.user = user

            result = f(*args, **kwargs)
            db.session.commit()

            return result

        return decorated_function

    return _login_required




def is_login():
    """判断是否登陆"""

    return "user" in g




def txid_format(txid):
    """格式化txid"""

    return txid.split("-")[0]


def format_name(name):
    """格式化名称"""

    return name.replace(" ", "_").lower()


def generate_captcha():
    """生成验证码"""

    random_digits = random.sample(string.digits, 6)
    random_list = random_digits

    random.shuffle(random_list)

    return "".join(random_list)


def camel_to_underline(camel_format):
    """驼峰命名格式转下划线命名格式"""

    underline_format = ''
    if isinstance(camel_format, str):
        for _s_ in camel_format:
            underline_format += _s_ if _s_.islower() else '_' + _s_.lower()
    return underline_format.lstrip("_")


def underline_to_camel(underline_format):
    """下划线命名格式驼峰命名格式"""

    camel_format = ''
    if isinstance(underline_format, str):
        for _s_ in underline_format.split('_'):
            camel_format += _s_.capitalize()
    return camel_format


def time_format(timestamp):
    """时间戳转datetime"""

    return datetime.datetime.fromtimestamp(int(timestamp))


def encode_decimal(o):
    if isinstance(o, Decimal):
        return float(round(o, 8))
    raise TypeError(repr(o) + " is not JSON serializable")


def generate_csv(datas, head, fields):
    """yield返回csv 内容"""
    head = ','.join(head) + '\n'
    yield head
    for data in datas:
        row = []
        for field in fields:
            row.append(str(data[field]))

        yield ','.join(row) + '\n'
