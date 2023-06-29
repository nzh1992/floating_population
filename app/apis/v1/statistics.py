# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/6/29
Last Modified: 2023/6/29
Description: 
"""
from flask import Blueprint, request
from sqlalchemy import extract

from app.apis import API_PREFIX
from app.core.jwt import JWTUtil
from app.models.population import Population
from app.extentions import siwadoc, db


statistic_bp = Blueprint('statistic', __name__, url_prefix=API_PREFIX + '/statistic')


@statistic_bp.route("/count_by_month", methods=["GET"])
@siwadoc.doc(tags=['statistic'], summary="按月流动人口统计")
@JWTUtil.verify_token_decorator(request)
def count_by_month(*args, **kwargs):
    month_list = list(range(1, 13))

    count_list = []
    for month in month_list:
        month_count = Population.query.filter(extract('month', Population.approval_time) == month).count()
        count_list.append(month_count)

    resp_data = {
        "data": count_list
    }

    return resp_data


@statistic_bp.route("/proportion_of_import", methods=["GET"])
@siwadoc.doc(tags=['statistic'], summary="流入流出占比")
@JWTUtil.verify_token_decorator(request)
def proportion_of_import(*args, **kwargs):
    import_count = Population.query.filter(Population.flow_status == 'IMPORT').count()
    export_count = Population.query.filter(Population.flow_status == 'EXPORT').count()

    resp_data = {
        "import": import_count,
        "export": export_count
    }

    return resp_data
