# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/6/7
Last Modified: 2023/6/7
Description: 
"""
import os

from flask import Blueprint, request, make_response

from app.apis import API_PREFIX
from app.extentions import siwadoc
from app.core.file_path import FilePath
from app.core.response import ErrorResponse


preview_bp = Blueprint('preview', __name__, url_prefix='/preview')


@preview_bp.route("/<uuid>/pictures/<image_name>", methods=["GET"])
@siwadoc.doc(tags=['preview'], summary="预览图片")
def preview_image(uuid, image_name):
    fp = FilePath.get_file_path_by_preview_url(uuid, "pictures", image_name)

    if not os.path.exists(fp):
        return ErrorResponse.image_not_found()

    # 根据图片类型设置Cnotent-Type
    _, file_extension = os.path.splitext(image_name)
    content_type_mapping = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
    }
    content_type = content_type_mapping.get(file_extension)

    # 读取图片二进制内容
    image_data = open(fp, 'rb').read()

    # 指定excel文件名
    resp = make_response(image_data)
    resp.headers["Content-Type"] = content_type

    return resp