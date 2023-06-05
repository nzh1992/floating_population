# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/6/5
Last Modified: 2023/6/5
Description: 
"""
import os
import shutil
import uuid

from flask import Blueprint, request, current_app

from app.core.file_path import FilePath
from app.core.jwt import JWTUtil
from app.core.response import ErrorResponse
from app.apis import API_PREFIX
from app.extentions import siwadoc


upload_bp = Blueprint('upload', __name__, url_prefix=API_PREFIX + '/upload')


@upload_bp.route("/image", methods=["POST"])
@siwadoc.doc(tags=['upload'], summary="上传图片")
@JWTUtil.verify_token_decorator(request)
def upload_picture(*args, **kwargs):
    upload_dir = FilePath.get_files_dir()

    # 临时文件分组id
    temp_file_uuid = str(uuid.uuid1())

    os.makedirs(upload_dir, exist_ok=True)

    file = request.files['file']

    file_name = file.filename
    _, file_extension = os.path.splitext(file_name)

    # 根据扩展名判断是否为图片类型
    valid_extension = ['.png', '.jpg', '.jpeg']
    if file_extension not in valid_extension:
        return ErrorResponse.upload_picture_type_error()

    save_fp = os.path.join(upload_dir, temp_file_uuid, "pictures", file_name)
    file.save(save_fp)

    # 下载url
    url = current_app.config['DOMAIN'] + f'/preview/{temp_file_uuid}/pictures/{file_name}'

    return {
        'url': url
    }


@upload_bp.route("/voiceprint", methods=["POST"])
@siwadoc.doc(tags=['upload'], summary="上传声纹")
@JWTUtil.verify_token_decorator(request)
def upload_voiceprint(*args, **kwargs):
    upload_dir = FilePath.get_files_dir()

    # 临时文件分组id
    temp_file_uuid = str(uuid.uuid1())

    os.makedirs(upload_dir, exist_ok=True)

    file = request.files['file']
    file_name = file.filename
    _, file_extension = os.path.splitext(file_name)

    # 根据扩展名判断是否为图片类型
    valid_extension = ['.mp3', '.wma', '.flac', '.acc', '.aiff']
    if file_extension not in valid_extension:
        return ErrorResponse.upload_voiceprint_type_error()

    save_fp = os.path.join(upload_dir, temp_file_uuid, "voiceprints", file_name)
    file.save(save_fp)

    # 下载url
    url = current_app.config['DOMAIN'] + f'/preview/{temp_file_uuid}/voiceprints/{file_name}'

    return {
        'url': url
    }