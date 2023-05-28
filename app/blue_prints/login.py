# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
from flask import Blueprint, request

from app.models.user import User
from app.extentions import db
from app.core.response import ErrorResponse


login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    account = request.form.get("account")
    password = request.form.get("password")

    user = User.query.filter(User.account == account).first()

    if not user:
        return ErrorResponse.login_user_not_exist(), 406

    if not user.check_password(password):
        return ErrorResponse.login_failed(), 406


@login_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json(force=True)
    account = data.get("account")
    password = data.get("password")

    user = User(account=account)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {'msg': 'ok'}