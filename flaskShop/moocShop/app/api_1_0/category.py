from app.api_1_0 import api
from app.model import categoryModel
from flask import jsonify
'''
获取所有分类信息
@url /category/all
http GET
'''
@api.route('/category/all')
def getAllCategory():
    category=categoryModel.getAllCategory()
    return jsonify(category)