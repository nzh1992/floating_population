# # -*- coding: utf-8 -*-
# """
# Author: niziheng
# Created Date: 2023/5/2
# Last Modified: 2023/5/2
# Description:
# """
# import click
# from flask import Flask, render_template, request, url_for, redirect, flash
#
# from flask_sqlalchemy import SQLAlchemy
#
#
# app = Flask(__name__)
#
# app.config['SECRET_KEY'] = 'dev'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Nzh199266!@localhost/floating_population?charset=utf8mb4"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
#
#
# class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
#     id = db.Column(db.Integer, primary_key=True)  # 主键
#     name = db.Column(db.String(20))  # 名字
#
#
# class Movie(db.Model):  # 表名将会是 movie
#     id = db.Column(db.Integer, primary_key=True)  # 主键
#     title = db.Column(db.String(60))  # 电影标题
#     year = db.Column(db.String(4))  # 电影年份
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @app.context_processor
# def inject_user():
#     """模板上下文注册函数"""
#     user = User.query.first()
#     return dict(user=user)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template("login.html")
#     else:
#         pass
#
#
# @app.route('/', methods=['GET', 'POST'])
# def hello():
#     if request.method == 'GET':
#         movies = Movie.query.all()
#         return render_template("index.html", movies=movies)
#     else:
#         title = request.form.get('title')
#         year = request.form.get('year')
#
#         if not title or not year or len(year) > 4 or len(title) > 60:
#             flash("无效输入")
#             return redirect(url_for('hello'))
#
#         movie = Movie(title=title, year=year)
#         db.session.add(movie)
#         db.session.commit()
#
#         flash("创建成功")
#         return redirect(url_for('hello'))
#
#
# @app.cli.command()
# @click.option('--drop', is_flag=True, help='Create after drop')
# def initdb(drop):
#     """初始化数据库"""
#     if drop:
#         db.drop_all()
#
#     db.create_all()
#     click.echo('Initailized database.')
#
#
# @app.cli.command()
# def forge():
#     """生成虚拟数据"""
#     db.create_all()
#
#     # 全局的两个变量移动到这个函数内
#     name = 'Grey Li'
#     movies = [
#         {'title': 'My Neighbor Totoro', 'year': '1988'},
#         {'title': 'Dead Poets Society', 'year': '1989'},
#         {'title': 'A Perfect World', 'year': '1993'},
#         {'title': 'Leon', 'year': '1994'},
#         {'title': 'Mahjong', 'year': '1996'},
#         {'title': 'Swallowtail Butterfly', 'year': '1996'},
#         {'title': 'King of Comedy', 'year': '1999'},
#         {'title': 'Devils on the Doorstep', 'year': '1999'},
#         {'title': 'WALL-E', 'year': '2008'},
#         {'title': 'The Pork of Music', 'year': '2012'},
#     ]
#
#     user = User(name=name)
#     db.session.add(user)
#
#     for m in movies:
#         movie = Movie(title=m['title'], year=m['year'])
#         db.session.add(movie)
#
#     db.session.commit()
#     click.echo("生成虚拟数据，完成.")