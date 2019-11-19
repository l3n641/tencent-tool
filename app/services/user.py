# -*- coding: utf-8 -*-

from .common import CommonService
from app.extensions import db


class UserService(CommonService):

    def get_by_account(self, account):
        """根据账号获取用户信息"""

        return self._model.query.filter(
            self._model.phone == account,
        ).first()

    def save(self, **kwargs):
        """注册新用户"""

        self.columns.append("password")
        user_id = CommonService.save(self, **kwargs)
        db.session.commit()
        return user_id
