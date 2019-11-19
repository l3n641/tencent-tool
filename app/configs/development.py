# -*- coding: utf-8 -*-

from .common import Common


class Config(Common):
    TESTING = True
    TRANS_COMMENT = "automation[dev]"
    SQLALCHEMY_ECHO = True

