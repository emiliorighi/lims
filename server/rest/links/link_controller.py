from flask_restful import Resource
from flask import Response, request
from . import link_service
from flask_jwt_extended import jwt_required
from wrappers import project_access
import json

class LinksAPI(Resource):
    def get(self):
        response, mimetype = link_service.get_links(request.args)
        return Response(response, mimetype=mimetype, status=200)

class ProjectModelLinksAPI(Resource):
    def get(self, project_id, model_name):
        response, mimetype = link_service.get_project_model_links(project_id, model_name, request.args)
        return Response(response, mimetype=mimetype, status=200)
    
    @jwt_required()
    @project_access.project_access_required()
    def post(self, project_id, model_name):
        files = request.files.getlist("files")
        metadata = request.form.to_dict(flat=False)        
        resp = link_service.upload_links(project_id, model_name, files,metadata)
        return Response(json.dumps(resp), mimetype="application/json", status=201)

class ProjectModelLinkAPI(Resource):
    @jwt_required()
    @project_access.project_access_required()
    def delete(self, project_id, model_name,type, name):
        resp = link_service.delete_link(project_id, model_name, name, type)
        return Response(resp, mimetype="application/json", status=201)
