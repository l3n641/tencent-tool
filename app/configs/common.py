# -*- coding: utf-8 -*-

import os



class Common:
    SECRET_KEY = os.getenv("SECRET_KEY")

    TRANS_COMMENT = "automation"
    WALLET_PASSWORD = os.getenv("WALLET_PASSWORD")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

