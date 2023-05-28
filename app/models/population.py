# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""
from app.extentions import db


class Population(db.Model):
    __tablename__ = "population"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))                        # 姓名
    age = db.Column(db.Integer)                             # 年龄
    sex = db.Column(db.String(128))                         # 性别
    birth = db.Column(db.DateTime)                          # 出生年月日
    academic_qualification = db.Column(db.String(128))      # 学历
    id_number = db.Column(db.String(128))                   # 身份证号
    address = db.Column(db.String(255))                     # 当前住址
    native_place_province = db.Column(db.String(128))       # 籍贯省
    native_place_city = db.Column(db.String(128))           # 籍贯市
    native_place_area = db.Column(db.String(128))           # 籍贯区
    marital_status = db.Column(db.String(128))              # 婚姻状况
    voiceprint_dir = db.Column(db.String(255))              # 声纹存放目录
    picture_dir = db.Column(db.String(255))                 # 图片存放目录
    submission_status = db.Column(db.String(128))           # 提交状态
    submission_time = db.Column(db.DateTime)                # 提交时间
    approval_status = db.Column(db.String(128))             # 审批状态
    approval_time = db.Column(db.DateTime)                  # 审批时间

    def __repr__(self):
        return f"<Menu id={self.id} name={self.name}>"
