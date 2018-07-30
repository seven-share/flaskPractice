from flask import Blueprint,jsonify

exceptions = Blueprint('exceptions', __name__)

class SomethingFault(Exception): 
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

@exceptions.app_errorhandler(SomethingFault)
def invalid_usage(error):
    res={
        'message':error.message
    }
    return jsonify(res),error.status_code
