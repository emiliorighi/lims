import json
from flask_restful import Resource
from flask import Response, request
from . import projects_service


class ProjectsApi(Resource):
    def get(self):
        total, data = projects_service.get_projects(**request.args)
        json_resp = dict(total=total,data=data)
        return Response(json.dumps(json_resp), mimetype="application/json", status=200)
    
    def post(self):
        data = request.json if request.is_json else request.form
        messages, status = projects_service.create_project(data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
    
class ProjectApi(Resource):
    def get(self, project_id):
        project = projects_service.get_project(project_id)
        return Response(project.to_json(), mimetype="application/json", status=200)
