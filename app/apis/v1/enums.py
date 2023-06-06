# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/6/6
Last Modified: 2023/6/6
Description: 
"""
from flask import Blueprint, request

from app.apis import API_PREFIX
from app.core.jwt import JWTUtil
from app.core.enums import AcademicEnum, MaritalEnum
from app.extentions import siwadoc, db


academic_bp = Blueprint('academic', __name__, url_prefix=API_PREFIX + '/academic')

marital_bp = Blueprint('marital', __name__, url_prefix=API_PREFIX + '/marital')


@academic_bp.route("/all", methods=["GET"])
@siwadoc.doc(tags=['academic'], summary="获取全部学历")
@JWTUtil.verify_token_decorator(request)
def all_academic(*args, **kwargs):
    resp_data = {
        'data': AcademicEnum
    }

    return resp_data


@marital_bp.route("/all", methods=["GET"])
@siwadoc.doc(tags=['marital'], summary="获取全部婚姻状况")
@JWTUtil.verify_token_decorator(request)
def all_academic(*args, **kwargs):
    resp_data = {
        'data': MaritalEnum
    }

    return resp_data