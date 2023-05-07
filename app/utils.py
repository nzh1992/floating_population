# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
import os


class FilePath:
    @classmethod
    def get_root_path(cls):
        root_path = os.path.dirname(os.path.dirname(__file__))
        return root_path

    @classmethod
    def get_template_folder(cls):
        template_folder = os.path.join(cls.get_root_path(), 'templates')
        return template_folder

    @classmethod
    def get_static_folder(cls):
        static_folder = os.path.join(cls.get_root_path(), 'static')
        return static_folder

    @classmethod
    def get_setting_fp(cls):
        setting_fp = os.path.join(cls.get_root_path(), 'app', 'setting.py')
        return setting_fp
