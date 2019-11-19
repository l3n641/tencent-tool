# -*- coding: utf-8 -*-

import logging

from flask import Flask

from app.extensions import bootstrap, db, migrate
from app.functions import get_module_functions, is_login, url_for, get_endpoint


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object("app.configs.%s.Config" % object_name)

    app.logger.setLevel(logging.INFO)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


    app.add_template_global(is_login)
    app.add_template_global(url_for)
    app.add_template_global(get_endpoint)

    return app
