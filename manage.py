# -*- coding: utf-8 -*-

import os

from flask import request
from flask.cli import load_dotenv
from app import models

from app import create_app

load_dotenv()
app = create_app(os.getenv("FLASK_ENV"))


@app.before_request
def before_request():
    app.jinja_env.cache = None
    if request.blueprint is not None:
        bp = app.blueprints[request.blueprint]
        if bp.jinja_loader is not None:
            newsearchpath = bp.jinja_loader.searchpath + app.jinja_loader.searchpath
            app.jinja_loader.searchpath = newsearchpath
        else:
            app.jinja_loader.searchpath = app.jinja_loader.searchpath[-1:]
    else:
        app.jinja_loader.searchpath = app.jinja_loader.searchpath[-1:]


@app.cli.command("create-user")
def create_user():
    """
    创建用户
    :return:
    """
    from app.services import user_srv

    print('开始创建账号')
    phone = input("输入用户的手机号:")

    data = user_srv.get_first({"phone": phone})

    while data is not None:
        phone = input("该号码已经存在了,请重新输入号码:")
        data = user_srv.get_first({"phone": phone})

    password = input("请输入登陆密码:")

    user_srv.save(**{"phone": phone, "password": password})
