from flask import request
from ..models import User
import base64
from werkzeug.security import check_password_hash

def basic_auth_required(func):
    def decorated(*args, **kargs):
        if "Authorization" in request.headers:
            val = request.headers["Authorization"]
            encoded_version = val.split()[1]
            credentials = base64.b64decode(encoded_version.encode('ascii')).decode('ascii')
            username, password = credentials.split(":")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                return {
                    'status': "ok",
                    'data': {}
                }
            else: 
                return {
                    'status': 'not ok',
                    'message': 'Invalid username/password'
                }, 400
        return {
            'status': 'not ok',
            'message': 'not a valid username'
        }, 400    




