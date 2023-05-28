# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
import json

from app.extentions import db


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))          # 角色名称
    menu_ids = db.Column(db.Text)            # 该角色可访问菜单的id列表

    def __repr__(self):
        return f"<Role id={self.id} name={self.name}>"

    @classmethod
    def init_db(cls):
        """初始化数据库调用"""
        # 管理员
        admin_menu_ids = json.dumps([])
        admin = cls(id=1, name="ADMIN", menu_ids=admin_menu_ids)

        # 录入员
        enter_menu_ids = json.dumps([])
        enter = cls(id=2, name="ENTER", menu_ids=enter_menu_ids)

        # 审批员
        approval_menu_ids = json.dumps([])
        approval = cls(id=3, name="APPROVAL", menu_ids=approval_menu_ids)

        db.session.add(admin)
        db.session.add(enter)
        db.session.add(approval)
        db.session.commit()
