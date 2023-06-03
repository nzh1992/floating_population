# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/30
Last Modified: 2023/5/30
Description: 
"""
from datetime import datetime


class DatetimeHelper:
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def __init__(self):
        pass

    @classmethod
    def get_current_datetime_str(cls):
        """
        获取当前时间的字符串格式，格式如"2023-05-01 00:00:00"
        """
        current_datetime = datetime.now().strftime(cls.DATETIME_FORMAT)
        return current_datetime

    @classmethod
    def get_datetime_str(cls, dt):
        """
        获取给定时间的字符串格式
        """
        dt_str = dt.strftime(cls.DATETIME_FORMAT)
        return dt_str