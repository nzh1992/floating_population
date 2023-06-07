# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""

DEBUG = True


SECRET_KEY = "dev"


# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Nzh199266!@localhost/floating_population?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@47.103.15.19/floating_population?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False


# DOMAIN = "http://47.103.15.19"
DOMAIN = "http://localhost:6500"

# 上传图片、声纹文件的最大值
# 注意Nginx上也要配置
MAX_CONTENT_LENGTH = 20 * 1024 * 1024
