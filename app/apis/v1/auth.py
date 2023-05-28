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
from app.core.api_params import LoginParam
from app.core.jwt import JWTUtil
from app.models.user import User
from app.apis import API_PREFIX


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

    resp_data = {
        'access_token': access_token,
        'token_expires': token_expires,
        'user_id': user.id,
        'user_name': user.user_name,
        'role_type': user.role_type
    }

    return Response.make_response(0, "", resp_data)
