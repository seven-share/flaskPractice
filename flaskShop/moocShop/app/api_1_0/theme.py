from app.api_1_0 import api
from app.validation import isAllInt,isInt,isNotFind
from flask import jsonify,request
from app.model import themeModel

'''
获取指定theme信息
@url /theme?ids=id1,id2,id3
@return 一组theme
http GET
'''
@api.route('/theme', methods=['GET'])
def getTheme():
  ids=request.values.get('ids')
  isNotFind('/theme?ids=id1,id2,id3',ids)
  ids = ids.split(',')
  isAllInt('/theme',ids)
  results=themeModel.getThemeList(ids)
  return jsonify(results)
'''
获取指定theme下的详细
@url /theme/<id>
http GET
'''
@api.route('/theme/<id>',methods=['GET'])
def getThemeDetail(id):
  isInt('/theme/<id>',id)
  result=themeModel.getThemeDetial(id)
  return jsonify(result)
