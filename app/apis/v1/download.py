# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/6/7
Last Modified: 2023/6/7
Description: 
"""
import os

from flask import Blueprint, request, send_from_directory

from app.apis import API_PREFIX
from app.extentions import siwadoc
from app.core.response import ErrorResponse
from app.core.file_path import FilePath


download_bp = Blueprint('download', __name__, url_prefix='/download')


@download_bp.route("/<uuid>/pictures/<image_name>", methods=["GET"])
@siwadoc.doc(tags=['download'], summary="下载图片")
def download_image(uuid, image_name):
    download_fp = FilePath.get_file_path_by_preview_url(uuid, "pictures", image_name)

    download_dir, _ = os.path.split(download_fp)

    if not os.path.exists(download_fp):
        return ErrorResponse.image_not_found()

    return send_from_directory(download_dir, image_name, as_attachment=True)


@download_bp.route("/<uuid>/voiceprints/<file_name>", methods=["GET"])
@siwadoc.doc(tags=['download'], summary="下载声纹")
def download_voiceprint(uuid, file_name):
    download_fp = FilePath.get_file_path_by_preview_url(uuid, "voiceprints", file_name)

    download_dir, _ = os.path.split(download_fp)

    if not os.path.exists(download_fp):
        return ErrorResponse.voiceprint_not_found()

    return send_from_directory(download_dir, file_name, as_attachment=True)