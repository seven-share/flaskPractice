from app.model.models import Product,Address,Order,User
from app.validation import noProduct,noAddress
from app import db
import json,time,random


def place(uid,oProducts):
    uid=uid
    oProducts=oProducts
    products = getProductsByOrder(oProducts)
    status=getOrderStatus(oProducts,products)
    if not status['pass']:
        status['order_id']=-1
        return status
    snap=snapOrder(status,uid)
    order=createOrder(snap,uid)
    order['pass']=True
    return order




def getProductsByOrder(oProducts):
    opID=[]
    for op in oProducts:
        opID.append(op['product_id'])
    products=Product.query.filter(Product.id.in_(opID)).all()
    return [pd.to_json() for pd in products]
def getOrderStatus(oProducts,products):
    status={
        'pass':True,
        'orderPrice':0,
        'totalCount':0,
        'pStatusList':[]
    }
    for op in oProducts:
        pStatus=getProductStatus(op,products)
        if pStatus['haveStock']==False:
            status['pass']=False
        status['orderPrice']+=pStatus['totalPrice']
        status['totalCount'] += pStatus['count']
        status['pStatusList'].append(pStatus)
    return status
def getProductStatus(op,products):
    pIndex=-1
    pStatus={
        'id':None,
        'haveStock':False,
        'count':0,
        'name':'',
        'price':0,
        'totalPrice':0,
        'main_img_url':''
    }
    for i in range(len(products)):
        if op['product_id']==products[i]['id']:
            pIndex=i
    if pIndex==-1:
        return noProduct('order',op['product_id'])
    else:
        product=products[pIndex]
        pStatus['id']=product['id']
        pStatus['count']=op['count']
        pStatus['name']=product['name']
        pStatus['price']=product['price']
        pStatus['totalPrice']=float(product['price'])*op['count']
        pStatus['main_img_url']=product['main_img_url']
        if product['stock']-op['count']>=0:
            pStatus['haveStock']=True
    return pStatus

def snapOrder(status,uid):
    snap={
        'orderPrice':0,
        'totalCount':0,
        'pStatus':[],
        'snapAddress':'',
        'snapName':'',
        'snapImg':''
    }
    snap['orderPrice']=status['orderPrice']
    snap['totalCount']=status['totalCount']
    snap['pStatus']=status['pStatusList']
    snap['snapAddress']=json.dumps(getUserAddress(uid))
    snap['snapName']=status['pStatusList'][0]['name']
    snap['snapImg'] = status['pStatusList'][0]['main_img_url']
    if len(status['pStatusList'])>1:
        snap['snapName']+='等'
    return snap

def getUserAddress(uid):
    address=Address.query.filter_by(user_id=uid).first()
    if not address:
        noAddress()
    address=address.to_json()
    return address
def createOrder(snap,uid):
    orderNo=makeOrderNo()
    order=Order()
    order.order_no=orderNo
    order.user=User.query.get(uid)
    order.total_price=snap['orderPrice']
    order.total_count=snap['totalCount']
    order.snap_img=snap['snapImg']
    order.snap_name=snap['snapName']
    order.snap_address=snap['snapAddress']
    order.snap_items=json.dumps(snap['pStatus'])
    db.session.add(order)
    db.session.commit()
    return {
        'orderNo':orderNo,
        'order_id':order.id,
        'create_time':str(order.create_time)
    }


def makeOrderNo():
    orderSn='A'+str(int(time.time()))+random.choice('abcdefghigklmnopqrstuvwxyz')+str(random.randint(0,99))
    return orderSn

def checkOrderStock(orderID):
    snap_items=Order.query.get(orderID).snap_items
    snap_items=json.loads(snap_items)
    oProducts=[]
    for item in snap_items:
        oProduct={
            'product_id':item['id'],
            'count':item['count']
        }
        oProducts.append(oProduct)
    products=getProductsByOrder(oProducts)
    status=getOrderStatus(oProducts,products)
    return status