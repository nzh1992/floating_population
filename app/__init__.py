# -*- coding: utf-8 -*-
"""
Author: niziheng
Created Date: 2023/5/6
Last Modified: 2023/5/6
Description: 
"""
import os
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

    create_files_dir()

    register_extentions(app)

    register_blue_print(app)

    register_commands(app)

    initdb(app)

    return app


def register_extentions(app):
    from .extentions import db
    from .extentions import siwadoc

    db.init_app(app)
    siwadoc.init_app(app)


def register_blue_print(app):
    from app.apis.v1.auth import auth_bp
    from app.apis.v1.role import role_bp
    from app.apis.v1.population import population_bp
    from app.apis.v1.user import user_bp
    from app.apis.v1.upload import upload_bp
    from app.apis.v1.region import region_bp
    from app.apis.v1.enums import academic_bp, marital_bp
    from app.apis.v1.audit_population import audit_bp
    from app.apis.v1.preview import preview_bp
    from app.apis.v1.download import download_bp
    from app.apis.v1.statistics import statistic_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(population_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(region_bp)
    app.register_blueprint(academic_bp)
    app.register_blueprint(marital_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(preview_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(statistic_bp)


def initdb(app, drop=None):
    """初始化数据库"""
    with app.app_context():
        from sqlalchemy import text
        from .extentions import db
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


def create_files_dir():
    """创建文件存放目录"""
    files_dir = FilePath.get_files_dir()
    os.makedirs(files_dir, exist_ok=True)