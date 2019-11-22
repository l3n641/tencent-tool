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
    from app.functions import generate_default_config

    print('开始创建账号')
    user_name = input("输入用户名:")

    data = user_srv.get_first({"user_name": user_name})

    while data is not None:
        user_name = input("该用户名已经存在了,请重新输入:")
        data = user_srv.get_first({"user_name": user_name})

    password = input("请输入登陆密码:")

    user_id = user_srv.save(**{"user_name": user_name, "password": password})
    if user_id:
        generate_default_config(user_id)
        print("注册用户成功")
