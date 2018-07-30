from .exceptions import SomethingFault
from flask import current_app
import re
'''
是否是整数
'''
def isInt(path,arg):
  try:
    arg = int(arg)
    if arg < 0:
      raise ValueError
  except:
    message = path + '--' + 'notInt'
    raise SomethingFault(message, 400)
'''
没有找到该数据
'''
def isNotFind(path,arg):
  if arg is None:
    message=path+'--'+'notFind'
    raise SomethingFault(message,300)
'''
是否全部是整数
'''
def isAllInt(path,args):
  for i in args:
    isInt(path,i)
'''
是否是在1到15之间
'''
def btProduct(path,arg):
  isInt(path,arg)
  if int(arg)>15 or int(arg)<1:
    message = path + '--' + 'not in 1-15'
    raise SomethingFault(message, 400)
def mustHave(path,arg):
  if not arg:
    message = path + '--' + 'empty or None'
    current_app.logger.warning(message)
    raise SomethingFault(message, 400)
# 微信登录获取openid
def wxLoginFail(path,arg):
  message = path + '--' + 'can not get openid'
  raise SomethingFault(message,400)
def badToken():
  message='bad token'
  raise SomethingFault(message,401)
def addressTest(addressData):
  try:
    mustHave('/address',addressData['name'])
    mustHave('/address',addressData['mobile'])
    isPhoneNumber(addressData['mobile'])
    mustHave('/address',addressData['province'])
    mustHave('/address', addressData['city'])
    mustHave('/address', addressData['country'])
    mustHave('/address', addressData['detail'])
  except:
    raise SomethingFault('address is bad')
def isPhoneNumber(num):
  # result=re.match('1[3458]\\d{9}',num)
  result=True
  if not result:
    raise SomethingFault('bad phoneNum',400)
def noScope():
  raise SomethingFault('token do not have scope', 401)
def notUserScope():
  raise SomethingFault('do not have user scope',401)
def success():
  raise SomethingFault('ok',200)

def checkProduct(products):
  if not isinstance(products,list):
    raise SomethingFault('product is not list', 400)
  if not products:
    raise SomethingFault('product is empty',400)
  for pd in products:
    isInt('/order',pd['product_id'])
    isInt('/order',pd['count'])

def noProduct(path,arg):
  message = path + '--'+'can not find product'
  raise SomethingFault(message,404)
def noAddress():
  raise SomethingFault('no that address',404)
def noOrder(path,arg):
  message = path + '--' + 'can not find order'
  raise SomethingFault(message, 404)
def notMatch(path,arg):
  message = path + '--' + 'user not match order'
  raise SomethingFault(message, 404)
def orderExcepiton(path,message):
  msg=path+'---'+message
  raise SomethingFault(msg,404)

