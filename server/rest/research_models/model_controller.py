import json
from flask_restful import Resource
from flask import Response, request
from . import model_service
from flask_jwt_extended import jwt_required
from wrappers import admin
from helpers import data as data_helper

class ModelsApi(Resource):
    def get(self):
        response, mimetype= model_service.get_models(request.args)
        return Response(response, mimetype=mimetype, status=200)
    
class ProjectModelsApi(Resource):
    def get(self, project_id):
        total, data = model_service.get_project_models(project_id, **request.args)
        json_resp = dict(total=total,data=data)
        return Response(data_helper.dump_json(json_resp), mimetype="application/json", status=200)
    
    @jwt_required()
    @admin.admin_required()
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        message = model_service.create_model(project_id, data)
        return Response(json.dumps(message), mimetype="application/json", status=201)
    
class EditModelFieldDescriptionApi(Resource):
    def put(self, project_id, model_name, field_key):
        data = request.json if request.is_json else request.form
        resp = model_service.update_field_description(project_id,model_name,field_key, data)
        return Response(json.dumps(resp), mimetype="application/json", status=201)

class ProjectModelApi(Resource):
    def get(self, project_id, model_name):
        project = model_service.get_project_model(project_id, model_name)
        return Response(data_helper.dump_json(project.to_mongo().to_dict()), mimetype="application/json", status=200)
    
    @jwt_required()
    @admin.admin_required()
    def delete(self, project_id, model_name):
        resp = model_service.delete_model(project_id, model_name)
        return Response(json.dumps(resp), mimetype="application/json", status=201)

    @jwt_required()
    @admin.admin_required()
    def put(self, project_id, model_name):
        data = request.json if request.is_json else request.form
        resp = model_service.update_model(project_id, model_name, data)
        return Response(json.dumps(resp), mimetype="application/json", status=201)


class RelatedModelRecordCount(Resource):
    def get(self, project_id, model_name):
        resp = model_service.get_records_count_of_related_models(project_id, model_name)
        return Response(json.dumps(resp), mimetype="application/json", status=201)
