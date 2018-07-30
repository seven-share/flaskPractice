from app.model.orderModel import checkOrderStock
from app.model.models import Order,Product
from app.validation import isInt
from app.validation import noOrder,notMatch,orderExcepiton
from flask import g,request
from app.wxPay import build_form_by_params
from app import db
import json
class OrderStatus():
    UNPAID=1
    PAID=2
    DELIVERED=3
    PAID_BUT_OUT_OF=4

def pay(orderID):
    order=checkOrderValid(orderID)
    orderNo=order.order_no
    isInt('/pre_order',orderID)
    status=checkOrderStock(orderID)
    if not status['pass']:
        return status
    pre_params=makeWxPreOrder(order)
    return pre_params
def checkOrderValid(orderID):
    order=Order.query.get(orderID)
    if not order:
        noOrder('/pre_order',order)
    if not order.user_id==g.user['id']:
        notMatch('/pre_order', g.user['id'])
    if not order.status==OrderStatus.UNPAID:
        orderExcepiton('/pre_order','have paid')
    return order
def makeWxPreOrder(order):
    openid=g.user['openid']
    if not openid:
        orderExcepiton('/pre_order','no openid')
    params={}
    params['body']='零食商店'
    params['attach']='深圳分店'
    params['out_trade_no']=order.order_no
    params['total_fee']=int(order.total_price*100)
    params['openid']=g.user['openid']
    params['spbill_create_ip']=request.remote_addr
    params= build_form_by_params(params)
    prepay_id=params['prepay_id']
    order.prepay_id=prepay_id
    db.session.add(order)
    db.session.commit()
    params.pop('prepay_id')
    return params


def notifyProcess(data):
    if data['result_code']=='SUCCESS':
        orderNo=data['out_trade_no']
        try:
            order=Order.query.filter_by(order_no=orderNo).first()
            stockStatus=checkOrderStock(order.id)
            if order.status==OrderStatus.UNPAID:
                order.status=OrderStatus.PAID
                db.session.add(order)
                reduceStock(stockStatus)
                db.session.commit()
            else:
                order.status = OrderStatus.PAID_BUT_OUT_OF
                db.session.add(order)
                db.session.commit()
            return True
        except :
            db.session.rollback()
            orderExcepiton('/pay/notify','notify wrong')
            return False




def reduceStock(stockStatus):
    pStatusList=json.loads(stockStatus['pStatusList'])
    for pl in pStatusList:
        product=Product.query.get(pl['id'])
        product.stock=product.stock-pl['count']
        db.session.add(product)






