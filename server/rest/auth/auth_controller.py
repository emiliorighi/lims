import json
from flask_restful import Resource
from flask import Response, request
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies
from datetime import timedelta
from db.models import User

class LoginApi(Resource):
    def post(self):
        payload = request.json if request.is_json else request.form
        if 'name' in payload.keys() and 'password' in payload.keys():
            name = payload['name']
            password = payload['password']
            user_obj = User.objects(name=name).first()
            if user_obj and user_obj.password == password:
                access_token = create_access_token(identity=name,expires_delta=timedelta(minutes=30))
                response = Response(json.dumps(dict(msg=f"welcome {name}",role=user_obj.role.value)), mimetype="application/json", status=200)
                set_access_cookies(response, access_token)
                return response     
        return Response(json.dumps({"msg":"Bad User or Password"}), mimetype="application/json", status=401)

class LogoutApi(Resource):
    @jwt_required()
    def get(self):
        response = Response(json.dumps({"msg":"Logout succesfull"}), mimetype="application/json", status=200)
        unset_jwt_cookies(response)
        return response

