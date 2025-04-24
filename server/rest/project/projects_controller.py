import json
from flask_restful import Resource
from flask import Response, request
from . import projects_service
from flask_jwt_extended import jwt_required
from wrappers import admin
from helpers import data as data_helper

class ResearchProjectsApi(Resource):
    def get(self):
        
        total, data = projects_service.get_projects(**request.args)
        json_resp = dict(total=total,data=data)
        return Response(data_helper.dump_json(json_resp), mimetype="application/json", status=200)
    
    @jwt_required()
    @admin.admin_required()
    def post(self):
        data = request.json if request.is_json else request.form
        format = 'yaml' if request.headers['Content-Type'] == 'application/x-yaml' else 'json'
        message = projects_service.create_project(data, format)
        return Response(json.dumps(message), mimetype="application/json", status=201)
    
class ResearchProjectApi(Resource):
    def get(self, project_id):
        project = projects_service.get_project(project_id)
        return Response(data_helper.dump_json(project.to_mongo().to_dict()), mimetype="application/json", status=200)

class ArchiveResearchProjectApi(Resource):
    @jwt_required()
    @admin.admin_required()
    def patch(self, project_id):
        resp = projects_service.archive_project(project_id)
        return Response(data_helper.dump_json(resp), mimetype="application/json", status=200)

class UnarchiveResearchProjectApi(Resource):
    @jwt_required()
    @admin.admin_required()
    def patch(self, project_id):
        resp = projects_service.unarchive_project(project_id)
        return Response(data_helper.dump_json(resp), mimetype="application/json", status=200)

class ResearchProjectSchema(Resource):
    def get(self, project_id):
        response = projects_service.get_project_schema(project_id)
        return Response(data_helper.dump_json(response), mimetype="application/json", status=200)
