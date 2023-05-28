# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
from app.extentions import db


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))          # 角色名称
    menu_ids = db.Column(db.Text)            # 该角色可访问菜单的id列表

    def __repr__(self):
        return f"<Role id={self.id} name={self.name}>"
