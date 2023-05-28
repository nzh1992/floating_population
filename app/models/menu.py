# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""
import json

from app.extentions import db


class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))          # 菜单名称
    parent_id = db.Column(db.Integer)            # 该角色可访问菜单的id列表

    def __repr__(self):
        return f"<Menu id={self.id} name={self.name}>"

    @classmethod
    def init_db(cls):
        """初始化数据库调用"""
        # 工作台(一级菜单)
        workbench = Menu(id=1, name="工作台", parent_id=0)

        db.session.add(workbench)
        db.session.commit()
