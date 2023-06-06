# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""
import os

from app.extentions import db
from app.core.file_path import FilePath


class Population(db.Model):
    __tablename__ = "population"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))                        # 姓名
    age = db.Column(db.Integer)                             # 年龄
    sex = db.Column(db.String(128))                         # 性别
    academic_qualification = db.Column(db.String(128))      # 学历
    id_number = db.Column(db.String(128))                   # 身份证号
    address = db.Column(db.Text)                            # 当前住址
    detail_address = db.Column(db.String(255))              # 当前详细住址
    native_place_province = db.Column(db.String(128))       # 籍贯省
    native_place_city = db.Column(db.String(128))           # 籍贯市
    native_place_area = db.Column(db.String(128))           # 籍贯区
    marital_status = db.Column(db.String(128))              # 婚姻状况
    voiceprint = db.Column(db.Text)                         # 声纹存放目录列表
    picture = db.Column(db.Text)                            # 图片存放目录列表
    enter_status = db.Column(db.String(128))                # 录入状态
    audit_status = db.Column(db.String(128))                # 审批状态
    reason = db.Column(db.String(255))                      # 拒绝原因
    submission_time = db.Column(db.DateTime)                # 提交时间
    approval_time = db.Column(db.DateTime)                  # 审批时间

    def __repr__(self):
        return f"<Population id={self.id} name={self.name}>"
