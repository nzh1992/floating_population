# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/6/6
Last Modified: 2023/6/6
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
from app.core.api_params import AddPopulationParam
from app.extentions import siwadoc, db
from app.models.population import Population


academic_bp = Blueprint('academic', __name__, url_prefix=API_PREFIX + '/academic')

marital_bp = Blueprint('marital', __name__, url_prefix=API_PREFIX + '/marital')


@academic_bp.route("/all", methods=["GET"])
@siwadoc.doc(tags=['academic'], summary="获取全部学历")
@JWTUtil.verify_token_decorator(request)
def all_academic(*args, **kwargs):
    academic_data = [
        {
            "name": "小学",
            "value": "1"
        },
        {
            "name": "初中",
            "value": "2"
        },
        {
            "name": "高中(职高、高技、中专）",
            "value": "3"
        },
        {
            "name": "大专",
            "value": "4"
        },
        {
            "name": "本科",
            "value": "5"
        },
        {
            "name": "硕士研究生",
            "value": "6"
        },
        {
            "name": "博士研究生",
            "value": "7"
        }
    ]

    resp_data = {
        'data': academic_data
    }

    return resp_data


@marital_bp.route("/all", methods=["GET"])
@siwadoc.doc(tags=['marital'], summary="获取全部婚姻状况")
@JWTUtil.verify_token_decorator(request)
def all_academic(*args, **kwargs):
    marital_data = [
        {
            "name": "已婚",
            "value": "1"
        },
        {
            "name": "未婚",
            "value": "2"
        },
        {
            "name": "离异/丧偶",
            "value": "3"
        }
    ]

    resp_data = {
        'data': marital_data
    }

    return resp_data