from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
import logging

db=SQLAlchemy()


def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)
  db.init_app(app)
  # # 注册授权服务蓝本
  # from .auth import auth as auth_blueprint
  # app.register_blueprint(auth_blueprint, url_prefix='/auth')

  # 注册REST Web服务蓝本
  from .api_1_0 import api as api_1_0_blueprint
  app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

  # 注册自定义异常
  from .exceptions import exceptions as exceptions_blueprint
  app.register_blueprint(exceptions_blueprint,url_prefix='/exceptions')
  # 日志记录系统
  handler = logging.FileHandler('logs/flask.log')
  handler.setLevel(logging.DEBUG)
  logging_format = logging.Formatter(
      '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
  handler.setFormatter(logging_format)
  app.logger.addHandler(handler)

  return app
