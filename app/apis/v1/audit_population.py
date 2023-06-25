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
from sqlalchemy import or_

from app.apis import API_PREFIX
from app.core.jwt import JWTUtil
from app.core.response import Response, ErrorResponse
from app.core.datetime_helper import DatetimeHelper
from app.core.log_helper import logger
from app.core.api_params import AddPopulationParam
from app.extentions import siwadoc, db
from app.models.population import Population
from app.core.enums import MaritalEnum


audit_bp = Blueprint('audit', __name__, url_prefix=API_PREFIX + '/audit')


@audit_bp.route("/list", methods=["POST"])
@siwadoc.doc(tags=['audit'], summary="审批列表")
@JWTUtil.verify_token_decorator(request)
def audit_population_list(*args, **kwargs):
    data = request.get_json(force=True)
    status = data.get("audit_status")
    keyword = data.get("keyword")
    native = data.get("native")
    flow_status = data.get("flow_status")
    pn = data.get("pn")
    pz = data.get("pz")

    # 过滤掉未审批的数据
    query_filter = Population.query.filter(Population.enter_status != "UN_AUDIT")

    if keyword:
        condition = or_(
            Population.name.like(f"%{keyword}%"),
            Population.id_number.like(f"%{keyword}%")
        )
        query_filter = query_filter.filter(condition)

    if status:
        query_filter = query_filter.filter(Population.audit_status == status)

    if native:
        query_filter = query_filter.filter(Population.native_place_province == native[0]) \
            .filter(Population.native_place_city == native[1]) \
            .filter(Population.native_place_area == native[2])

    if flow_status:
        query_filter = query_filter.filter(Population.flow_status == flow_status)

    total = query_filter.count()

    start = (pn - 1) * pz
    populations = query_filter.limit(pz).offset(start).all()

    serialize_population_list = []
    for population in populations:
        # 查询婚姻状况枚举
        marital = [m for m in MaritalEnum if m.get("value") == population.marital_status][0]

        population_data = {
            "id": population.id,
            "name": population.name,
            "age": population.age,
            "gender": population.sex,
            "marital_status": marital,
            "id_number": population.id_number,
            "native": [population.native_place_province, population.native_place_city, population.native_place_area],
            "audit_status": population.audit_status,
            "reason": population.reason,
            "flow_status": population.flow_status
        }
        serialize_population_list.append(population_data)

    resp_data = {
        "total": total,
        "list": serialize_population_list
    }

    return resp_data


@audit_bp.route("/<id>", methods=["GET"])
@siwadoc.doc(tags=['audit'], summary="查看流动人口详情")
@JWTUtil.verify_token_decorator(request)
def audit_population_detail(*args, **kwargs):
    population_id = args[1].get("id")

    population = Population.query.filter(Population.id == population_id).first()
    if not population:
        return ErrorResponse.population_not_found()

    population_data = {
        "name": population.name,
        "age": population.age,
        "gender": population.sex,
        "academic_qualification": population.academic_qualification,
        "marital_status": population.marital_status,
        "id_number": population.id_number,
        "native": [population.native_place_province, population.native_place_city, population.native_place_area],
        "address": json.loads(population.address),
        "detail_address": population.detail_address,
        "voiceprint": json.loads(population.voiceprint),
        "picture": json.loads(population.picture),
        "audit_status": population.audit_status,
        "reason": population.reason,
        "flow_status": population.flow_status
    }

    return population_data


@audit_bp.route("/resolve", methods=["POST"])
@siwadoc.doc(tags=['audit'], summary="审批通过")
@JWTUtil.verify_token_decorator(request)
def audit_resolve(*args, **kwargs):
    data = request.get_json(force=True)
    population_id = data.get("id")

    population = Population.query.filter(Population.id == population_id).first()
    if not population:
        return ErrorResponse.population_not_found()

    population.enter_status = "RESOLVE"
    population.audit_status = "RESOLVE"
    population.reason = None
    population.approval_time = DatetimeHelper.get_datetime_str(datetime.datetime.now())

    db.session.add(population)
    db.session.commit()

    return {}


@audit_bp.route("/reject", methods=["POST"])
@siwadoc.doc(tags=['audit'], summary="审批拒绝")
@JWTUtil.verify_token_decorator(request)
def audit_reject(*args, **kwargs):
    data = request.get_json(force=True)
    population_id = data.get("id")
    reason = data.get("reason")

    population = Population.query.filter(Population.id == population_id).first()
    if not population:
        return ErrorResponse.population_not_found()

    population.enter_status = "REJECT"
    population.audit_status = "REJECT"
    population.reason = reason
    population.approval_time = DatetimeHelper.get_datetime_str(datetime.datetime.now())

    db.session.add(population)
    db.session.commit()

    return {}