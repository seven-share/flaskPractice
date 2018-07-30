from app.api_1_0 import api
from flask import request,jsonify
from app.model import productModel
from app.validation import btProduct,isInt
'''
获取近期product
@url /product/recent?count=1
http GET
'''
@api.route('/product/recent',methods=['GET'])
def getRecentProduct():
    count=request.values.get('count')
    if count is None:
        count=15
    btProduct('/product/recent',count)
    recentProducts=productModel.getRecentProducts(count)
    return jsonify(recentProducts)
'''
获取分类下的product
@url /product/by_category?id=2
http GET
'''
@api.route('/product/by_category',methods=['GET'])
def getAllInCategory():
    id=request.values.get('id')
    isInt('/product/by_category',id)
    allInCategory=productModel.getProductsByCategoryID(id)
    return jsonify(allInCategory)
'''
获取某个product的详细信息
@url /product/1
http GET
'''
@api.route('/product/<id>',methods=['GET'])
def getOne(id):
    isInt('/product/<id>',id)
    productDetail=productModel.getProductDetail(id)
    return jsonify(productDetail)


