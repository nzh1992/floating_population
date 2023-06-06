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


audit_bp = Blueprint('audit', __name__, url_prefix=API_PREFIX + '/audit')


@population_bp.route("/list", methods=["POST"])
@siwadoc.doc(tags=['population'], summary="创建流动人口", body=AddPopulationParam)
@JWTUtil.verify_token_decorator(request)
def audit_population_list(*args, **kwargs):
    pass