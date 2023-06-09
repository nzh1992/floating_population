# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""
from typing import Union, List

from flask_siwadoc import BaseModel


####################################################
# Auth
####################################################
class LoginParam(BaseModel):
    account: str
    password: str


class RegisterParam(BaseModel):
    account: str
    password: str
    user_name: str
    phone: Union[str, None]
    role_id: int


####################################################
# User
####################################################
class UserListParam(BaseModel):
    role_type: Union[str, None]
    keyword: Union[str, None]
    pn: int
    pz: int


####################################################
# Role
####################################################
class GetRoleDetailParam(BaseModel):
    id: int


####################################################
# Population
####################################################
class AddPopulationParam(BaseModel):
    id: Union[int, None]
    # 姓名
    name: str
    # 年龄
    age: Union[int, None]
    # 性别
    gender: str
    # 学历
    academic_qualification: str
    # 婚姻状况
    marital_status: str
    # 身份证号
    id_number: str
    # 籍贯省市区
    native: List
    # 当前住址
    address: List
    # 当前住址
    detail_address: str

