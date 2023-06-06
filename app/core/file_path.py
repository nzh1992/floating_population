# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/28
Last Modified: 2023/5/28
Description: 
"""
import os


class FilePath:
    @classmethod
    def get_root_path(cls):
        root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return root_path

    @classmethod
    def get_setting_fp(cls):
        setting_fp = os.path.join(cls.get_root_path(), 'app', 'setting.py')
        return setting_fp

    @classmethod
    def get_logger_fp(cls):
        logger_fp = ""

    @classmethod
    def get_files_dir(cls):
        """获取上传文件路径"""
        file_dir = os.path.join(cls.get_root_path(), "files")
        return file_dir

    @classmethod
    def get_region_file_path(cls):
        """获取省市区文件路径"""
        file_path = os.path.join(cls.get_root_path(), "region", "最新县及县以上行政区划代码.txt")
        return file_path