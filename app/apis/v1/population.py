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

from app.apis import API_PREFIX
from app.core.jwt import JWTUtil
from app.core.response import Response, ErrorResponse
from app.core.datetime_helper import DatetimeHelper
from app.core.log_helper import logger
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
    sex = data.get("sex")
    birth = data.get("birth")
    academic_qualification = data.get("academic_qualification")
    id_number = data.get("id_number")
    address = data.get("address")
    native_place_province = data.get("native_place_province")
    native_place_city = data.get("native_place_city")
    native_place_area = data.get("native_place_area")
    marital_status = data.get("marital_status")

    # 保存方式
    save_type = data.get("save_type")    # "保存" 或 "保存并提交"

    # 提交时间
    if save_type == "保存并提交":
        submission_status = "已提交"
        submission_time = DatetimeHelper.get_current_datetime_str()
    else:
        submission_status = "未提交"
        submission_time = None

    # 审批状态，默认为"未审批"
    approval_status = "未审批"

    population = Population(name=name, age=age, sex=sex, birth=birth, academic_qualification=academic_qualification,
                            id_number=id_number, address=address, native_place_province=native_place_province,
                            native_place_city=native_place_city, native_place_area=native_place_area,
                            marital_status=marital_status, submission_status=submission_status,
                            submission_time=submission_time, approval_status=approval_status)

    db.session.add(population)
    db.session.flush()

    # 数据库生成id，更新图片和声纹存放路径
    population.set_picture_dir()
    population.set_voiceprint_dir()

    db.session.add(population)
    db.session.commit()

    return Response.make_response(0, "ok")


@population_bp.route("/<id>", methods=["PATCH"])
@siwadoc.doc(tags=['population'], summary="修改流动人口", body=AddPopulationParam)
@JWTUtil.verify_token_decorator(request)
def modify_population(*args, **kwargs):
    population_id = args[1].get("id")

    data = request.get_json(force=True)

    # 流动人口基本信息
    name = data.get("name")
    age = data.get("age")
    sex = data.get("sex")
    birth = data.get("birth")
    academic_qualification = data.get("academic_qualification")
    id_number = data.get("id_number")
    address = data.get("address")
    native_place_province = data.get("native_place_province")
    native_place_city = data.get("native_place_city")
    native_place_area = data.get("native_place_area")
    marital_status = data.get("marital_status")

    # 保存方式
    save_type = data.get("save_type")  # "保存" 或 "保存并提交"

    # 提交时间
    if save_type == "保存并提交":
        submission_status = "已提交"
        submission_time = DatetimeHelper.get_current_datetime_str()
    else:
        submission_status = "未提交"
        submission_time = None

    # 审批状态，默认为"未审批"
    approval_status = "未审批"

    population = Population(name=name, age=age, sex=sex, birth=birth, academic_qualification=academic_qualification,
                            id_number=id_number, address=address, native_place_province=native_place_province,
                            native_place_city=native_place_city, native_place_area=native_place_area,
                            marital_status=marital_status, submission_status=submission_status,
                            submission_time=submission_time, approval_status=approval_status)
    db.session.add(population)
    db.session.commit()

    return Response.make_response(0, "ok")


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
        "sex": population.sex,
        "birth": DatetimeHelper.get_datetime_str(population.birth),
        "academic_qualification": population.academic_qualification,
        "id_number": population.id_number,
        "address": population.address,
        "native_place_province": population.native_place_province,
        "native_place_city": population.native_place_city,
        "native_place_area": population.native_place_area,
        "marital_status": population.marital_status
    }

    return Response.make_response(0, "ok", population_data)