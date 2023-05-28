# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
from werkzeug.security import generate_password_hash, check_password_hash

from app.extentions import db
from app.models.role import Role


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(128))                    # 登录账号
    password_hash = db.Column(db.String(128))              # 密码
    user_name = db.Column(db.String(128))                  # 姓名
    phone = db.Column(db.String(128))                      # 手机号
    role_id = db.Column(db.Integer, default=None)          # 角色id

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        is_right = check_password_hash(self.password_hash, password)
        return is_right

    def get_role(self):
        role = Role.query.filter(Role.id == self.role_id).first()
        return role