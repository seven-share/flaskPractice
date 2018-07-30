from flask import Blueprint

api = Blueprint('api', __name__)

from . import banner,theme,product,category,token,address,order,pay
