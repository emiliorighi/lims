import json
from flask_restful import Resource
from flask import Response, request
import yaml
from errors import NotFound
from db.models import Project
from . import projects_service


"""
CREATE PROJECT FROM YAML
CREATE PROJECT FROM JSON

"""

class ProjectsApi(Resource):
    def get(self):
        schema = open('/server/projects/gencode-schema.yaml', 'r')
        project =yaml.load(schema, yaml.SafeLoader)
        errors = projects_service.validate_project(project)
        if errors:
            print(errors)
        # total, data = projects_service.get_projects(**request.args)
        # json_resp = dict(total=total,data=list(data.as_pymongo()))
        # return Response(json.dumps(json_resp), mimetype="application/json", status=200)
    """
    expected payload fields:
        -format: yaml or json, default json
        -url: str | null
        -schema
    """
    def post(self):
        data = request.json if request.is_json else request.form
        response, status = projects_service.parse_project_payload(**data)
        return Response(json.dumps(response), mimetype="application/json", status=status)
    # def get(self):

class ProjectApi(Resource):
    def get(self, id):
        project = projects_service.get_project(id)
        return Response(project.to_json(), mimetype="application/json", status=200)
 
    # def put(self,id):
    # def delete(self,id):

        # return Response(json.dumps({"msg":"Bad User or Password"}), mimetype="application/json", status=401)

# class ProjectApi(Resource):
#     def get(self, name):
#         response = Response(json.dumps({"msg":"Logout succesfull"}), mimetype="application/json", status=200)
#         unset_jwt_cookies(response)
#         return response

