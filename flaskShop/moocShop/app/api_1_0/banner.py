from . import api
from app.model import bannerModel
from ..validation import isInt
from flask import jsonify,request
import json

'''
获取指定id的banner信息
id banner的id号
http GET
'''
@api.route('/banner/<id>', methods=['GET'])
def getBanner(id):
  isInt('/banner/<id>',id)
  banner_items=bannerModel.getBannerByid(id)
  return jsonify(banner_items)
