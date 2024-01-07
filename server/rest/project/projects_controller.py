import json
from flask_restful import Resource
from flask import Response, request
import yaml
from errors import NotFound
from db.models import Project
from . import projects_service

class ProjectsApi(Resource):
    def get(self):
        total, data = projects_service.get_projects(**request.args)
        json_resp = dict(total=total,data=list(data.as_pymongo()))
        return Response(json.dumps(json_resp), mimetype="application/json", status=200)

    def post(self):

        Project.drop_collection()
        schema = open('/server/projects/gencode-schema.yaml', 'r')
        project =yaml.load(schema, yaml.SafeLoader)
        project['version'] = str(project['version'])
        project_to_save = Project(**project)
        project_to_save.save()
        print(project_to_save.to_json())
    # def get(self):

class ProjectApi(Resource):
    def get(self, id):
        project = projects_service.get_project(id)
        return Response(project, mimetype="application/json", status=200)
 
    # def put(self,id):
    # def delete(self,id):

        # return Response(json.dumps({"msg":"Bad User or Password"}), mimetype="application/json", status=401)

# class ProjectApi(Resource):
#     def get(self, name):
#         response = Response(json.dumps({"msg":"Logout succesfull"}), mimetype="application/json", status=200)
#         unset_jwt_cookies(response)
#         return response

