from datetime import timedelta
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import Response
import json

def set_token(user):
    access_token = create_access_token(identity={'name': user.name, 'role': user.role.value}, expires_delta=timedelta(minutes=2))
    message = f"welcome {user.name}"
    response = Response(json.dumps(message), mimetype="application/json", status=200)
    set_access_cookies(response, access_token)
    return response
    