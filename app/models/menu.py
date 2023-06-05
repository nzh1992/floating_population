# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""
import json

from app.extentions import db
from app.core.log_helper import logger


class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))              # 菜单名称
    router = db.Column(db.String(128))            # 路由
    parent_id = db.Column(db.Integer)             # 该角色可访问菜单的id列表

    def __repr__(self):
        return f"<Menu id={self.id} name={self.name}>"

    @classmethod
    def init_db(cls):
        """初始化数据库调用"""
        menus = Menu.query.filter().all()
        menu_ids = [m.id for m in menus]

        # 工作台(一级菜单)
        workbench = Menu(id=1, name="工作台", router="/workbench", parent_id=0)
        # 录入管理
        enter = Menu(id=2, name="录入管理", router="/enterManage", parent_id=0)
        # 审批管理
        approval = Menu(id=3, name="审批管理", router="/approvalManage", parent_id=0)
        # 用户管理
        user_manage = Menu(id=4, name="用户管理", router="/userManage", parent_id=0)

        if workbench.id not in menu_ids:
            db.session.add(workbench)
            logger.info("初始化--菜单--工作台, 完成。")
        if enter.id not in menu_ids:
            db.session.add(enter)
            logger.info("初始化--菜单--录入管理, 完成。")
        if approval.id not in menu_ids:
            db.session.add(approval)
            logger.info("初始化--菜单--审批管理, 完成。")
        if user_manage.id not in menu_ids:
            db.session.add(user_manage)
            logger.info("初始化--菜单--用户管理, 完成。")

        db.session.commit()
        logger.info("全部菜单初始化, 完成。")
