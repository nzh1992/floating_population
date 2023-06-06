# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/6/6
Last Modified: 2023/6/6
Description: 
"""
import json

from flask import Blueprint, request

from app.apis import API_PREFIX
from app.extentions import siwadoc
from app.core.jwt import JWTUtil
from app.core.file_path import FilePath


region_bp = Blueprint('region', __name__, url_prefix=API_PREFIX + '/region')


@region_bp.route("/all", methods=["GET"])
@siwadoc.doc(tags=['region'], summary="获取行政区域列表")
@JWTUtil.verify_token_decorator(request)
def all_region(*args, **kwargs):
    region_fp = FilePath.get_region_file_path()
    with open(region_fp, 'r') as f:
        data = f.read()
        json_data = json.loads(data)

        # 全部
        resp = {
            'data': json_data
        }
        return resp
