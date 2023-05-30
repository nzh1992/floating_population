# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""
import json
import datetime

from flask import Blueprint, request

from app.apis import API_PREFIX
from app.core.jwt import JWTUtil
from app.core.response import Response, ErrorResponse
from app.core.log_helper import logger
from app.core.api_params import GetRoleDetailParam
from app.extentions import siwadoc, db
from app.models.role import Role
from app.models.menu import Menu


role_bp = Blueprint('role', __name__, url_prefix=API_PREFIX + '/role')


@role_bp.route("/<id>", methods=["GET"])
@siwadoc.doc(tags=['role'], summary="根据角色id查询可访问菜单")
@JWTUtil.verify_token_decorator(request)
def add_client(*args, **kwargs):
    role_id = args[1].get("id")
    role = Role.query.filter(Role.id == role_id).first()
    if not role:
        logger.error(f"查询角色失败，role_id: {role_id}")
        return ErrorResponse.role_not_found()

    # 角色数据
    role_data = {
        "id": role.id,
        "name": role.name
    }

    # 查询相关菜单
    menu_ids = json.loads(role.menu_ids)
    menus = Menu.query.filter(Menu.id.in_(menu_ids)).all()
    access_menus = []
    for menu in menus:
        access_menu_data = {
            "id": menu.id,
            "name": menu.name,
            "menu": menu.router,
            "children": []
        }
        access_menus.append(access_menu_data)

    role_data.update({"access": access_menus})

    return Response.make_response(0, "ok", role_data)