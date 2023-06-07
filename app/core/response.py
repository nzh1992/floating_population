# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""


def make_response(code, msg, data=None):
    resp = {
        "code": code,
        "msg": msg
    }

    if data:
        resp["data"] = data

    return resp


class Response:
    @classmethod
    def make_response(cls, code, msg, data=None):
        return make_response(code, msg, data)


class ErrorResponse:

    @staticmethod
    def login_user_not_exist():
        return make_response(1001, "登录用户名不存在"), 406

    @staticmethod
    def login_failed():
        return make_response(1002, "用户名或密码错误"), 406

    @staticmethod
    def request_missing_token():
        return make_response(1003, "请求头缺少token"), 401

    @staticmethod
    def request_token_expired():
        return make_response(1004, "token过期"), 401

    @staticmethod
    def request_token_error():
        return make_response(1005, "token错误"), 401

    @staticmethod
    def role_not_found():
        return make_response(1006, "角色不存在"), 406

    @staticmethod
    def population_not_found():
        return make_response(1007, "流动人口不存在"), 406

    @staticmethod
    def upload_picture_type_error():
        return make_response(1008, "上传图片类型错误"), 406

    @staticmethod
    def upload_voiceprint_type_error():
        return make_response(1009, "上传声纹类型错误"), 406

    @staticmethod
    def user_not_found():
        return make_response(1010, "用户不存在"), 406

    @staticmethod
    def populaiton_id_number_duplicate():
        return make_response(1011, "身份证号码重复"), 406