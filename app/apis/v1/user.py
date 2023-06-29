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
from app.core.datetime_helper import DatetimeHelper
from app.core.log_helper import logger
from app.core.api_params import UserListParam
from app.extentions import siwadoc, db
from app.models.user import User
from app.models.role import Role


user_bp = Blueprint('user', __name__, url_prefix=API_PREFIX + '/user')


@user_bp.route("/list", methods=["POST"])
@siwadoc.doc(tags=['user'], summary="用户列表", body=UserListParam)
@JWTUtil.verify_token_decorator(request)
def user_list(*args, **kwargs):
    data = request.get_json(force=True)
    role_type = data.get("role_type")
    keyword = data.get("keyword")
    pn = data.get("pn")
    pz = data.get("pz")

    query_filter = User.query.filter()

    if role_type:
        role = Role.query.filter(Role.name == role_type).first()
        query_filter = query_filter.filter(User.role_id == role.id)

    if keyword:
        query_filter.filter(User.user_name.like(f"%{keyword}%"))

    total = query_filter.count()

    start = (pn - 1) * pz
    users = query_filter.limit(pz).offset(start).all()

    serialize_user_list = []
    for user in users:
        role = Role.query.filter(Role.id == user.role_id).first()
        user_data = {
            "id": user.id,
            "account": user.account,
            "name": user.user_name,
            "role_type": role.name
        }
        serialize_user_list.append(user_data)

    resp_data = {
        "total": total,
        "list": serialize_user_list
    }

    return resp_data


@user_bp.route("/<id>", methods=["DELETE"])
@siwadoc.doc(tags=['user'], summary="删除用户")
@JWTUtil.verify_token_decorator(request)
def delete_user(*args, **kwargs):
    user_id = args[1].get("id")
    user = User.query.filter(User.id == user_id).first()
    if not user:
        return ErrorResponse.user_not_found()

    db.session.delete(user)
    db.session.commit()

    return {}


@user_bp.route("/", methods=["PUT"])
@siwadoc.doc(tags=['user'], summary="创建用户")
@JWTUtil.verify_token_decorator(request)
def create_user(*args, **kwargs):
    data = request.get_json(force=True)
    name = data.get("name")
    account = data.get("account")
    password = data.get("password")
    role_type = data.get("role_type")

    # 查询role
    role = Role.query.filter(Role.name == role_type).first()

    # 检查账号是否存在
    account_is_exist = User.query.filter(User.account == account).first()
    if account_is_exist:
        return ErrorResponse.account_exist()

    user = User(account=account, user_name=name, phone=None, role_id=role.id)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    resp_data = {

    }
    return resp_data


@user_bp.route("/<id>", methods=["GET"])
@siwadoc.doc(tags=['user'], summary="用户详情")
@JWTUtil.verify_token_decorator(request)
def user_detail(*args, **kwargs):
    user_id = args[1].get("id")

    user = User.query.filter(User.id == user_id).first()

    # role_type
    role = Role.query.filter(Role.id == user.role_id).first()

    user_data = {
        "id": user.id,
        "name": user.user_name,
        "account": user.account,
        "role_type": role.name
    }

    return user_data


@user_bp.route("/<id>", methods=["PATCH"])
@siwadoc.doc(tags=['user'], summary="修改用户")
@JWTUtil.verify_token_decorator(request)
def modify_user(*args, **kwargs):
    user_id = args[1].get("id")

    data = request.get_json(force=True)
    name = data.get("name")
    account = data.get("account")
    password = data.get("password")
    role_type = data.get("role_type")

    user = User.query.filter(User.id == user_id).first()

    # 查询role
    role = Role.query.filter(Role.name == role_type).first()

    # 检查账号是否存在
    account_is_exist = User.query.filter(User.id != user_id).filter(User.account == account).first()
    if account_is_exist:
        return ErrorResponse.account_exist()

    # 更新
    user.user_name = name
    user.account = account
    user.role_id = role.id

    if password:
        user.set_password(password)

    db.session.add(user)
    db.session.commit()

    resp_data = {

    }
    return resp_data