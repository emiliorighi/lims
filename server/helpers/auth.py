from datetime import timedelta
from helpers import data as data_helper
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import Response
import json

def set_token(user):
    access_token = create_access_token(identity=user,expires_delta=timedelta(days=30),additional_claims={"role": user.get('role'), "username":user.get('name')})
    response = Response(data_helper.dump_json(user), mimetype="application/json", status=200)
    set_access_cookies(response, access_token)
    return response
    