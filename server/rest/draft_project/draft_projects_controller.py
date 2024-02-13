import json
from flask_restful import Resource
from flask import Response, request
from . import draft_projects_service

class DraftProjectsApi(Resource):
    def get(self):
        total, data = draft_projects_service.get_draft_projects(**request.args)
        json_resp = dict(total=total,data=list(data.as_pymongo()))
        return Response(json.dumps(json_resp), mimetype="application/json", status=200)
    
    def post(self):
        data = request.json if request.is_json else request.form
        print(data.keys())
        message,status = draft_projects_service.create_draft_project(data)
        return Response(json.dumps(message), mimetype="application/json", status=status)
    
class DraftProjectApi(Resource):
    def get(self,project_id):
        project = draft_projects_service.get_draft_project(project_id)
        print(project)
        return Response(json.dumps(project), mimetype="application/json", status=200)

    def put(self,project_id):
        data = request.json if request.is_json else request.form
        message,status = draft_projects_service.update_draft_project(project_id,data)
        return Response(json.dumps(message), mimetype="application/json", status=status)
