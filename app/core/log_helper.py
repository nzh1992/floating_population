# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2022/9/27
Last Modified: 2022/9/27
Description: 系统运行日志
"""
import os

import loguru

from app.core.file_path import FilePath

# 日志存放路径
PROJECT_ROOT = FilePath.get_root_path()
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
LOG_FILE_NAME = "log_{time:YYYY-MM-DD}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# 日志等级
LOG_LEVEL = "INFO"

# 日志格式
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {file} | {line} | {message}"

# 日志回滚周期
LOG_ROTATION = "00:00"      # 每天0点回滚

# 日志保留天数
LOG_RETENTION = "15 days"

# 日志文件压缩格式
LOG_COMPRESSION = "zip"

# 日志文本编码
LOG_ENCODING = 'utf-8'

# 日志是否记录完整堆栈信息
LOG_BACKTRACE = True

# 日志是否记录异常诊断
LOG_DIAGNOSE = True


# 添加配置
loguru.logger.add(LOG_FILE_PATH, rotation=LOG_ROTATION, encoding=LOG_ENCODING,
                  enqueue=True, retention=LOG_RETENTION, compression=LOG_COMPRESSION,
                  format=LOG_FORMAT, level=LOG_LEVEL, backtrace=LOG_BACKTRACE,
                  diagnose=LOG_DIAGNOSE)

logger = loguru.logger
