import json
from flask_restful import Resource
from flask import Response, request
from . import draft_projects_service
from flask_jwt_extended import jwt_required
from wrappers import admin

class DraftProjectsApi(Resource):
    def get(self):
        total, data = draft_projects_service.get_draft_projects(**request.args)
        json_resp = dict(total=total,data=list(data.as_pymongo()))
        return Response(json.dumps(json_resp), mimetype="application/json", status=200)

    @jwt_required()
    @admin.admin_required()
    def post(self):
        data = request.json if request.is_json else request.form
        message,status = draft_projects_service.create_draft_project(data)
        return Response(json.dumps(message), mimetype="application/json", status=status)
    
class DraftProjectApi(Resource):
    def get(self,project_id):
        project = draft_projects_service.get_draft_project(project_id)
        return Response(project.to_json(), mimetype="application/json", status=200)

    @jwt_required()
    @admin.admin_required()
    def put(self,project_id):
        data = request.json if request.is_json else request.form
        message,status = draft_projects_service.update_draft_project(project_id,data)
        return Response(json.dumps(message), mimetype="application/json", status=status)

class ValidateProjectApi(Resource):
    def post(self):
        format = 'json'
        if request.headers['Content-Type'] == 'application/x-yaml':
            format = 'yaml'
        messages, status = draft_projects_service.validate_project(request.data,format)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class TsvUploadMapApi(Resource):
    def post(self):
        data = request.json if request.is_json else request.form
        attributes = draft_projects_service.map_attributes_from_tsv(request.files.get('tsv'),data)
        return Response(json.dumps(attributes), mimetype="application/json", status=200)
