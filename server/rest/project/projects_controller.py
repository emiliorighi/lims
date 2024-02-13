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
    
    """
    expected payload fields:
        -format: yaml or json, default json
        -url: str | null
        -schema
    """
    def post(self):
        data = request.json if request.is_json else request.form
        messages, status = projects_service.create_project(data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
    # def get(self):

class ProjectApi(Resource):
    def get(self, project_id):
        project = projects_service.get_project(project_id)
        return Response(json.dumps(project), mimetype="application/json", status=200)
