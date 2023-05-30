# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
import click
from flask import Flask

from app.core.file_path import FilePath
from app.models.user import User
from app.models.role import Role
from app.models.menu import Menu
from app.models.population import Population


def create_app():
    app = Flask(__name__,)

    setting_fp = FilePath.get_setting_fp()
    app.config.from_pyfile(setting_fp)

    register_extentions(app)

    register_blue_print(app)

    register_commands(app)

    return app


def register_extentions(app):
    from .extentions import db
    from .extentions import siwadoc

    db.init_app(app)
    siwadoc.init_app(app)


def register_blue_print(app):
    from app.apis.v1.auth import auth_bp
    from app.apis.v1.role import role_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(role_bp)


def register_commands(app):
    from app.extentions import db
    from app.models.menu import Menu
    from app.models.role import Role

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

        # 创建表
        db.create_all()
        click.echo("Create Tables, ok.")

        # 初始化表
        Menu.init_db()
        Role.init_db()
        click.echo("Initialized Tables, ok.")
