from datetime import timedelta
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import Response
import json

def set_token(user):
    access_token = create_access_token(identity=user, expires_delta=timedelta(days=7))
    resp={
        "user":user,
        "message":f"welcome {user['name']}"
    }
    response = Response(json.dumps(resp), mimetype="application/json", status=200)
    set_access_cookies(response, access_token)
    return response
    