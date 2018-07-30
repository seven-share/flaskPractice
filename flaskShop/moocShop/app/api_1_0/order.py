from app.api_1_0 import api
from app.model.userModel import auth,userRoleRequire
from app.model import orderModel
from app.model.models import Order
from app.validation import checkProduct,isInt,isNotFind
from flask import request,g
import json
from flask import jsonify
'''
下单接口
@url /order
http POST
所传数据类型
{
	"products":[

	{
		"product_id":1,
		"count":1
	},
	{
		"product_id":2,
		"count":3
	}
]
}
'''
@api.route('/order',methods=['POST'])
@auth.login_required
@userRoleRequire
def placeOrder():
    products=json.loads(request.data)['products']
    checkProduct(products)
    uid=g.user['id']
    status=orderModel.place(uid,products)
    return jsonify(status)
'''
获取用户历史订单分页信息
@url /order/by_user?page=2&size=4
http GET
'''
@api.route('/order/by_user',methods=['GET'])
@auth.login_required
@userRoleRequire
def getSummeryByUser():
    page =int(request.values.get('page') or 1)
    size=int(request.values.get('size') or 3)

    isInt('/order/by_user',page)
    isInt('/order/by_user', size)

    uid=g.user['id']
    pagination=Order.query.filter_by(user_id=uid).order_by(Order.create_time.desc()).paginate(
        page,per_page=size,error_out=False
    )
    ordersSummery=[ summery_to_json(od) for od in pagination.items]
    result={
        'ordersSummery':ordersSummery,
        'current_page':pagination.page
    }
    return jsonify(result)

def summery_to_json(od):
    order = {
        'id':od.id,
        'order_no': od.order_no,
        'total_price': str(od.total_price),
        'status': od.status,
        'snap_img': od.snap_img,
        'snap_name': od.snap_name,
        'total_count': od.total_count,
        'create_time':str(od.create_time)
    }
    return order
'''
获取某个订单的详细信息
@url /order/2
http GET
'''
@api.route('/order/<id>',methods=['GET'])
@auth.login_required
@userRoleRequire
def getOrderDetail(id):
    isInt('/order/<id>',id)
    id=int(id)
    order=Order.query.get(id)
    isNotFind('/order/<id>',order)
    order=order.to_json()
    return jsonify(order)
