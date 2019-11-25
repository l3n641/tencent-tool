# -*- coding: utf-8 -*-

import datetime
import importlib
import pkgutil
import random
import string
from decimal import Decimal
from functools import wraps
from inspect import getmembers, isfunction

from flask import g, redirect, request, session, url_for as origin_url_for

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
    """判断是否登录"""

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


def generate_default_config(user_id):
    from app.services import config_srv
    from app.extensions import db
    default_connfigs = [
        {"argument_key": "A76", "argument_description": "meeting_code", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "A67", "argument_description": "process_name", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "A49", "argument_description": "分支", "type": "string", "pre_argument": "", "user_id": user_id},
        {"argument_key": "A3", "argument_description": "device_id", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "A23", "argument_description": "发布渠道", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "A106", "argument_description": "设备显示名", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "A1", "argument_description": "app_uid", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "A8", "argument_description": "vip_level", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "A9", "argument_description": "product_name", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "os_ver", "argument_description": "操作系统版本号", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "unique_report_id", "argument_description": "log_id", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "wemeet_platform", "argument_description": "平台类型", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "A95", "argument_description": "app_id", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "background", "argument_description": "后台状态", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "role_type", "argument_description": "角色身份", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "meeting_type", "argument_description": "会议类型", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "av_room_id", "argument_description": "媒体房间号", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "account_type", "argument_description": "账户类型", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "corp_id", "argument_description": "公司id", "type": "string", "pre_argument": "",
         "user_id": user_id},
        {"argument_key": "app_main_version", "argument_description": "app版本号", "type": "string", "pre_argument": "",
         "user_id": user_id},

    ]

    for config in default_connfigs:
        config_srv.save(**config)
        db.session.commit()


def allowed_file(filename, extensions):
    """
    判断文件后缀是否运行
    :param filename:
    :param extensions:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extensions
