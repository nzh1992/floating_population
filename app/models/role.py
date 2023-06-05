# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
import json

from app.extentions import db
from app.core.log_helper import logger


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
        roles = Role.query.filter().all()
        role_ids = [r.id for r in roles]

        # 管理员
        admin_menu_ids = json.dumps([1,2,3])
        admin = cls(id=1, name="ADMIN", menu_ids=admin_menu_ids)

        # 录入员
        enter_menu_ids = json.dumps([1,2])
        enter = cls(id=2, name="ENTER", menu_ids=enter_menu_ids)

        # 审批员
        approval_menu_ids = json.dumps([1,3])
        approval = cls(id=3, name="AUDIT", menu_ids=approval_menu_ids)

        if admin.id not in role_ids:
            db.session.add(admin)
            logger.info("初始化--角色--管理员, 完成。")
        if enter.id not in role_ids:
            db.session.add(enter)
            logger.info("初始化--角色--录入员, 完成。")
        if approval.id not in role_ids:
            db.session.add(approval)
            logger.info("初始化--角色--审批员, 完成。")

        db.session.commit()
        logger.info("全部角色初始化, 完成。")
