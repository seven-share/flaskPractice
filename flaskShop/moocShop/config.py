#!/usr/bin/env python
# coding=utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  MCH_ID = '1443221402'
  UPLOAD_FOLDER = '/home/ubuntu/SweetHeart/imgs/upload'
  ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG',  'jpeg', 'gif'])

  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JSON_AS_ASCII=False
  IMG_PREFIX='http://localhost:5000/static/img'
  SECRET_KEY = os.environ.get('SECRET_KEY') or '5bf030dbb13422031ea802a9ab75900a'
  API_KEY = os.environ.get('API_KEY') or '666ZhangWangLuTin00SweetHeart999'

  APP_ID = 'wx1ed9ac6f29a707c1'
  APP_SECRET='c8eabf799dbf8a1362e9aba21825d20d'
  LOGIN_URL='https://api.weixin.qq.com/sns/jscode2session'
  
  @staticmethod
  def init_app(app):
    pass

# 三个环境可以设置不同的数据库
class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = 'mysql://root:1509980@localhost/zerg?charset=utf8'

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'mysql://hjy:hjy@localhost/SHTest?charset=utf8'

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'mysql://hjy:hjy@localhost/SweetHeart?charset=utf8'

# 通过config[name]来选择不同的配置环境
config = {
  'development' : DevelopmentConfig,
  'testing' : TestingConfig,
  'production' : ProductionConfig,
  'default' : DevelopmentConfig
}
