# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/4/24
Last Modified: 2023/4/24
Description: 
"""
import time
import datetime
from functools import wraps

import jwt
from jwt.exceptions import PyJWTError

from app.models.user import User
from app.core.log_helper import logger
from app.core.response import ErrorResponse


class JWTUtil:
    token_expire_time = 3600 * 12       # token过期时间，12小时
    secret = 'secret'                   # 秘钥
    algorithm = 'HS256'                 # 加密算法

    @classmethod
    def create_token(cls, user_id):
        """
        创建token

        :param user_id: int. 用户id
        """
        # 当前UTC时间戳
        utc_timestamp = time.mktime(datetime.datetime.utcnow().utctimetuple())
        # 过期UTC时间戳(秒)
        utc_expire_time = utc_timestamp + cls.token_expire_time
        # 秒转为毫秒
        utc_expire_time_ms = utc_expire_time * 1000

        payload = {
            'id': user_id,
            'token_expires': utc_expire_time_ms
        }
        token = jwt.encode(payload, cls.secret, algorithm=cls.algorithm)

        payload.update({'access_token': token})

        return payload

    @classmethod
    def verify_token(cls, token):
        """
        检查token是否合法（函数调用）

        :param token: str.
        :return: 返回值中code为枚举值，0成功，1token错误，2token过期
        """
        try:
            # 解析token
            payload = jwt.decode(token, cls.secret, algorithms=[cls.algorithm])
        except PyJWTError:
            logger.exception("Token解析失败")
            return {'result': False, 'msg': "Token解析失败", "code": 1}

        # 校验过期时间
        token_expires = payload.get("token_expires")
        current_utc_timestamp = time.mktime(datetime.datetime.utcnow().utctimetuple())
        if current_utc_timestamp > token_expires:
            logger.error("Token过期")
            return {'result': False, 'msg': "Token过期", 'code': 2}

        return {'result': True, 'msg': "Token合法", 'id': payload.get('id'), 'code': 0}

    @classmethod
    def verify_token_decorator(cls, request):
        """
        检查token是否合法（装饰器调用）
        """
        def decorated(func):

            @wraps(func)
            def wrapper(*args, **kwargs):
                token = request.headers.get("token")

                # 如果header中没有，再到查询参数中找
                if not token:
                    token = request.args.get("token")

                # 如果查询参数中也没有，报错处理
                if not token:
                    return ErrorResponse.request_missing_token()

                try:
                    result = cls.verify_token(token)

                    if result.get("code") == 1:
                        return ErrorResponse.request_token_error()
                    elif result.get("code") == 2:
                        return ErrorResponse.request_token_expired()
                    elif result.get("code") == 0:
                        user = User.query.filter(User.id == result.get("id")).first()
                        request.user = user

                    return func(args, kwargs)
                except jwt.ExpiredSignatureError as e:
                    raise e
                except Exception as e:
                    raise e

                return result

            return wrapper

        return decorated
