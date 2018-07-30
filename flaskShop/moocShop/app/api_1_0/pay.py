from app.api_1_0 import api
from app.model.userModel import auth,userRoleRequire
from app.model import payModel
from flask import request,jsonify
import json

@api.route('/pay/pre_order',methods=['POST'])
@auth.login_required
@userRoleRequire
def getPreOrder():
    orderID = json.loads(request.data)['id']
    pre_params = payModel.pay(orderID)
    return jsonify(pre_params)

@api.route('/pay/notify',methods=['POST'])
def receiveNotify():
    data=request.data
    payModel.notifyProcess(data)