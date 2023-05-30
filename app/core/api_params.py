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



####################################################
# Role
####################################################
class GetRoleDetailParam(BaseModel):
    id: int
