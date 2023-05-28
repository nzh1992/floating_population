# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""
from typing import Union, List

from flask_siwadoc import BaseModel


class LoginParam(BaseModel):
    account: str
    password: str


