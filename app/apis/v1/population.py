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
from sqlalchemy import or_

from app.apis import API_PREFIX
from app.core.jwt import JWTUtil
from app.core.response import Response, ErrorResponse
from app.core.enums import MaritalEnum
from app.core.api_params import AddPopulationParam
from app.extentions import siwadoc, db
from app.models.population import Population


population_bp = Blueprint('population', __name__, url_prefix=API_PREFIX + '/population')


@population_bp.route("/", methods=["PUT"])
@siwadoc.doc(tags=['population'], summary="创建流动人口", body=AddPopulationParam)
@JWTUtil.verify_token_decorator(request)
def add_population(*args, **kwargs):
    data = request.get_json(force=True)

    # 流动人口基本信息
    name = data.get("name")
    age = data.get("age")
    sex = data.get("gender")
    academic_qualification = data.get("academic_qualification")
    marital_status = data.get("marital_status")
    id_number = data.get("id_number")
    native = data.get("native")
    native_place_province = native[0]
    native_place_city = native[1]
    native_place_area = native[2]
    address = data.get("address")
    address_json = json.dumps(address)
    detail_address = data.get("detail_address")
    voiceprint = data.get("voiceprint")
    picture = data.get("picture")

    voiceprint_json = json.dumps(voiceprint)
    picture_json = json.dumps(picture)

    # 默认提交状态为"未审批"
    enter_status = "UN_AUDIT"
    audit_status = "UN_AUDIT"

    population = Population(name=name, age=age, sex=sex, academic_qualification=academic_qualification,
                            id_number=id_number, address=address_json, detail_address=detail_address,
                            native_place_province=native_place_province, native_place_city=native_place_city,
                            native_place_area=native_place_area, marital_status=marital_status,
                            enter_status=enter_status, audit_status=audit_status, voiceprint=voiceprint_json,
                            picture=picture_json)

    db.session.add(population)
    db.session.flush()
    db.session.commit()

    resp_data = {"id": population.id}
    return resp_data


@population_bp.route("/<id>", methods=["PATCH"])
@siwadoc.doc(tags=['population'], summary="修改流动人口", body=AddPopulationParam)
@JWTUtil.verify_token_decorator(request)
def modify_population(*args, **kwargs):
    population_id = args[1].get("id")
    population = Population.query.filter(Population.id == population_id).first()
    if not population:
        return ErrorResponse.population_not_found()

    data = request.get_json(force=True)

    # 流动人口基本信息
    name = data.get("name")
    age = data.get("age")
    sex = data.get("gender")
    academic_qualification = data.get("academic_qualification")
    marital_status = data.get("marital_status")
    id_number = data.get("id_number")
    native = data.get("native")
    native_place_province = native[0]
    native_place_city = native[1]
    native_place_area = native[2]
    address = data.get("address")
    detail_address = data.get("detail_address")
    voiceprint = data.get("voiceprint")
    picture = data.get("picture")

    voiceprint_json = json.dumps(voiceprint)
    picture_json = json.dumps(picture)

    # 更新人口信息
    population.name = name
    population.age = age
    population.sex = sex
    population.academic_qualification = academic_qualification
    population.marital_status = marital_status
    population.id_number = id_number
    population.native_place_province = native_place_province
    population.native_place_city = native_place_city
    population.native_place_area = native_place_area
    population.address = json.dumps(address)
    population.detail_address = detail_address
    population.voiceprint = voiceprint_json
    population.picture = picture_json

    db.session.add(population)
    db.session.commit()

    resp_data = {"id": population.id}
    return resp_data


@population_bp.route("/<id>", methods=["GET"])
@siwadoc.doc(tags=['population'], summary="查看流动人口")
@JWTUtil.verify_token_decorator(request)
def population_detail(*args, **kwargs):
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
        "enter_status": population.enter_status,
        "reason": population.reason
    }

    resp_data = {
        "data": population_data
    }
    return resp_data


@population_bp.route("/list", methods=["POST"])
@siwadoc.doc(tags=['population'], summary="流动人口列表")
@JWTUtil.verify_token_decorator(request)
def population_list(*args, **kwargs):
    data = request.get_json(force=True)
    keyword = data.get("keyword")
    audit_status = data.get("audit_status")
    native = data.get("native")
    pn = data.get("pn")
    pz = data.get("pz")

    query_filter = Population.query.filter()

    if keyword:
        condition = or_(
            Population.name.like(f"%{keyword}%"),
            Population.id_number.like(f"%{keyword}%")
        )
        query_filter.filter(condition)

    if audit_status:
        query_filter.filter(Population.status == audit_status)

    if native:
        query_filter.filter(Population.native_place_province == native[0])\
            .filter(Population.native_place_city == native[1])\
            .filter(Population.native_place_area == native[2])

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
            "enter_status": population.enter_status,
            "reason": population.reason
        }
        serialize_population_list.append(population_data)

    resp_data = {
        "total": total,
        "list": serialize_population_list
    }

    return resp_data


@population_bp.route("/<id>", methods=["DELETE"])
@siwadoc.doc(tags=['population'], summary="删除流动人口")
@JWTUtil.verify_token_decorator(request)
def delete_population(*args, **kwargs):
    population_id = args[1].get("id")

    population = Population.query.filter(Population.id == population_id).first()
    if not population:
        return ErrorResponse.population_not_found()

    db.session.delete(population)
    db.session.commit()

    return {}


@population_bp.route("/submit", methods=["POST"])
@siwadoc.doc(tags=['population'], summary="提交")
@JWTUtil.verify_token_decorator(request)
def submit_population(*args, **kwargs):
    data = request.get_json(force=True)
    population_id = data.get("id")

    population = Population.query.filter(Population.id == population_id).first()
    if not population:
        return ErrorResponse.population_not_found()

    population.enter_status = "AUDITING"

    db.session.add(population)
    db.session.commit()

    return {}