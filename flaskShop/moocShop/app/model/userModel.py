from app.model.models import User
from flask import current_app,g
import requests
from app.validation import mustHave,wxLoginFail,badToken,noScope,notUserScope
from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_httpauth import HTTPTokenAuth
from functools import wraps
class Role():
    User=16
    Super=32
def getToken(code):
    wxAppID=current_app.config.get('APP_ID')
    wxAppSecret=current_app.config.get('APP_SECRET')
    wxLoginUrl=current_app.config.get('LOGIN_URL')

    data = {}
    data['appid'] = wxAppID
    data['secret'] = wxAppSecret
    data['js_code'] = code
    data['grant_type'] = 'authorization_code'
    result = requests.get(wxLoginUrl, params=data).json()
    mustHave('/token/user',result)
    if 'errcode' in result.keys():
        wxLoginFail('/token/user',result)
    else:
        token=grantToken(result)
        return token

def grantToken(result):
    openid=result['openid']
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        user = User(openid=openid)
        db.session.add(user)
        db.session.commit()
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=7200)
    token=s.dumps({'id':user.id,'openid':user.openid,'scope':Role.User})
    return token

auth=HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    g.user = None
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=7200)
    try:
        data = s.loads(token)
    except:
        return False
    if 'openid' in data:
        g.user = data
        return True
    return False

@auth.error_handler
def auth_error():
    badToken()

def userRoleRequire(fun):
    @wraps(fun)
    def decoreate(*args,**kwargs):
        scope=g.user['scope']
        if not scope:
            noScope()
        if scope<Role.User:
            notUserScope()
        return fun(*args,**kwargs)
    return decoreate
