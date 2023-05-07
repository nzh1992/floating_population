# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
from flask import Blueprint, request, render_template, flash

from app.models.user import User
from app.extentions import db


login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    render_data = {}

    if request.method == 'GET':
        return render_template("login.html", render_data=render_data)
    else:
        account = request.form.get("account")
        password = request.form.get("password")

        user = User.query.filter(User.account == account).first()

        if not user:
            render_data["msg"] = "用户不存在"
            return render_template("login.html", render_data=render_data)

        if not user.check_password(password):
            render_data["msg"] = "密码错误"
            return render_template("login.html", render_data=render_data)

        return render_template("index.html")


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