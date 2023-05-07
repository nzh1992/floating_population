# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
import click
from flask import Flask

from .utils import FilePath
from app.models.user import User
from app.models.role import Role


def create_app():
    # 模板路径
    template_folder = FilePath.get_template_folder()
    # 静态资源路径
    static_folder = FilePath.get_static_folder()
    # 配置文件路径
    serring_fp = FilePath.get_setting_fp()

    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    app.config.from_pyfile(serring_fp)

    register_extentions(app)

    register_blue_print(app)

    register_commands(app)

    return app


def register_extentions(app):
    from .extentions import db

    db.init_app(app)


def register_blue_print(app):
    from app.blue_prints.login import login_bp

    app.register_blueprint(login_bp)


def register_commands(app):
    from app.extentions import db

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        """初始化数据库"""
        from sqlalchemy import text
        cursor = db.session.execute(text("show databases;"))
        result = [row[0] for row in cursor]
        print(result)

        if drop:
            db.drop_all()

        db.create_all()
        click.echo('Initailized database.')