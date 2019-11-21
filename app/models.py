# -*- coding: utf-8 -*-

from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    modified_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    delete_time = db.Column(db.DateTime, nullable=True)


class User(Base):
    """用户表"""

    phone = db.Column(db.String(255), unique=True, nullable=True, index=True)  # 手机号
    password_hash = db.Column(db.String(255), nullable=False)  # 密码

    @property
    def username(self):
        return self.phone

    @property
    def password(self):
        raise AttributeError("password is not readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Config(Base):
    argument_key = db.Column(db.String(255), unique=False, nullable=False)
    argument_description = db.Column(db.String(255), unique=False, nullable=False)
    type = db.Column(db.String(255), unique=False, nullable=False)
    pre_argument = db.Column(db.String(255), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
