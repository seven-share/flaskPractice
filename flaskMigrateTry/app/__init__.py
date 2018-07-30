from flask import Flask
from config import config
from app.models.base import db
# import app.models.wordRepertory
from app.models.wordRepertory import CET4

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # import app.models.wordRepertory

    # from app.models.wordRepertory import CET4,CET6

    
    db.init_app(app)
    db.create_all(app=app)
    
    
    from app.api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint,url_prefix='/api/v1.0')    


    return app

