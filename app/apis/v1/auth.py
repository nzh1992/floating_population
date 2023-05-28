# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""
from typing import Union
import datetime

from flask import Blueprint, request, current_app

from app.extentions import siwadoc
from app.core.response import Response, ErrorResponse
from app.core.api_params import LoginParam, RegisterParam
from app.core.jwt import JWTUtil
from app.models.user import User
from app.apis import API_PREFIX
from app.extentions import db


auth_bp = Blueprint('auth', __name__, url_prefix=API_PREFIX + '/auth')


@auth_bp.route('/login', methods=["POST"])
@siwadoc.doc(tags=['auth'], summary="登录", body=LoginParam)
def login():
    data = request.get_json(force=True)
    account = data.get("account")
    password = data.get("password")

    user = User.query.filter(User.account == account).first()

    if not user:
        return ErrorResponse.login_user_not_exist(), 406

    if not user.check_password(password):
        return ErrorResponse.login_failed(), 406

    # 生成token
    access_token_data = JWTUtil.create_token(user.id)
    access_token = access_token_data.get("access_token")
    token_expires = access_token_data.get("token_expires")

    role = user.get_role()

    resp_data = {
        'access_token': access_token,
        'token_expires': token_expires,
        'user_id': user.id,
        'user_name': user.user_name,
        'role_type': role.name
    }

    return Response.make_response(0, "", resp_data)


@auth_bp.route('/register', methods=["POST"])
@siwadoc.doc(tags=['auth'], summary="注册账号", body=LoginParam)
def register():
    data = request.get_json(force=True)
    account = data.get("account")
    password = data.get("password")
    user_name = data.get("user_name")
    phone = data.get("phone")
    role_id = data.get("role_id")

    user = User(account=account, user_name=user_name, phone=phone, role_id=role_id)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return Response.make_response(0, "ok")