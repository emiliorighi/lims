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
        total, data = projects_service.get_projects(**request.args)
        json_resp = dict(total=total,data=list(data.as_pymongo()))
        return Response(json.dumps(json_resp), mimetype="application/json", status=200)
    
    def post(self):
        data = request.json if request.is_json else request.form
        messages, status = projects_service.create_project(data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

##returns the list of mapped attributes
class TsvUploadApi(Resource):
    def post(self):
        data = request.json if request.is_json else request.form
        attributes = projects_service.map_attributes_from_tsv(request.files.get('tsv'),data)
        return Response(json.dumps(attributes), mimetype="application/json", status=200)

class ProjectApi(Resource):
    def get(self, project_id):
        project = projects_service.get_project(project_id)
        return Response(json.dumps(project), mimetype="application/json", status=200)


class ValidateProjectApi(Resource):
    def post(self):
        format = 'json'
        if request.headers['Content-Type'] == 'application/x-yaml':
            format = 'yaml'
        messages, status = projects_service.validate_project(request.data,format)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
