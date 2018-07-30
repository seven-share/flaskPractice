from app.api_1_0 import api
from app.model.userModel import auth,userRoleRequire
from app.model.models import User, Address
from flask import request,g,jsonify
from app.validation import mustHave, addressTest,success,noAddress
from app import db
import json
'''
保存用户地址等信息

http POST
数据格式
{
	"name":"wo小童",
	"mobile":"13202039670",
	"province":"河北",
	"city":"邯郸",
	"country":"中国",
	"detail":"细节，恭喜发财,我想你"
}
'''
@api.route('/address',methods=['POST'])
@auth.login_required
@userRoleRequire
def createOrUpdateAddress():
    id=g.user['id']
    user=User.query.get(id)
    mustHave('/address,user',user)
    addressData = json.loads(request.data,encoding="utf-8")
    addressTest(addressData)
    address=Address.query.filter_by(user_id=id).first()
    if not address:
        address=Address()
        address.name=addressData['name']
        address.mobile=addressData['mobile']
        address.province=addressData['province']
        address.city=addressData['city']
        address.country=addressData['country']
        address.detail=addressData['detail']
        address.user=user
        db.session.add(address)
        db.session.commit()
    else:
        address.name = addressData['name']
        address.mobile = addressData['mobile']
        address.province = addressData['province']
        address.city = addressData['city']
        address.country = addressData['country']
        address.detail = addressData['detail']
        db.session.add(address)
        db.session.commit()
    success()


@api.route('/address',methods=['GET'])
@auth.login_required
@userRoleRequire
def getUserAddress():
    id = g.user['id']
    address = Address.query.filter_by(user_id=id).first()
    if not address:
        noAddress()
    else:
        return jsonify(address.to_json())