import json
from . import users_service
from flask_restful import Resource
from flask import Response, request
from flask_jwt_extended import jwt_required, unset_jwt_cookies, get_jwt_identity
from helpers import auth

class LoginApi(Resource):
    #check if user alredy logged in
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return Response(json.dumps(current_user), 200)

    def post(self):
        payload = request.json if request.is_json else request.form
        name = payload.get('name')
        pwd = payload.get('password')
        if not name or not pwd:
            return Response(json.dumps("name or password are required"), mimetype="application/json", status=400)
        user = users_service.get_user(name,pwd)
        response = auth.set_token(user)
        return response

class LogoutApi(Resource):
    @jwt_required()
    def get(self):
        response = Response(json.dumps({"msg":"Logout succesfull"}), mimetype="application/json", status=200)
        unset_jwt_cookies(response)
        return response

class UsersApi(Resource):

    @jwt_required()
    def get(self):
        total, data = users_service.get_users(**request.args)
        json_resp = dict(total=total,data=list(data.as_pymongo()))
        return Response(json.dumps(json_resp), mimetype="application/json", status=200)

    ##create user
    @jwt_required()
    def post(self):
        data = request.json if request.is_json else request.form
        message, status = users_service.create_user(data)
        return Response(json.dumps(message), mimetype="application/json", status=status)


class UserApi(Resource):


    
    @jwt_required()
    def put(self,name):
        data = request.json if request.is_json else request.form
        message, status = users_service.update_user(name,data)
        return Response(json.dumps(message), mimetype="application/json", status=status)


    @jwt_required()
    def delete(self,name):
        message, status = users_service.delete_user(name)
        return Response(json.dumps(message), mimetype="application/json", status=status)
