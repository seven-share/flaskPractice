from app.api_1_0 import api
from flask import request,jsonify

@api.route('/hello', methods=['GET'])
def getToken():
    

    return jsonify('nihao')
