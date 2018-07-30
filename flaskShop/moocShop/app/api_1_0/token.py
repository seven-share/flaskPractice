from app.api_1_0 import api
from app.validation import mustHave
from flask import request,jsonify
from app.model import userModel
import json
@api.route('/token/user', methods=['POST'])
def getToken():
    code=json.loads(request.data)['code']
    mustHave('/token/user', code)
    token=userModel.getToken(code)
    token=token.decode("utf-8")
    return jsonify({'token':token})

@api.route('/token/verify', methods=['POST'])
def verifyToken():
    token = json.loads(request.data)['token']
    verify=userModel.verify_token(token)
    if not verify:
        return jsonify({'isValid':False})
    else:
        return jsonify({'isValid':True})
@api.route('/token/app_token', methods=['POST'])
def getAppToken():
    data=json.loads(request.data)
    ac=data['ac']
    se=data['se']
    mustHave('/token/user', ac)
    mustHave('/token/user', se)
