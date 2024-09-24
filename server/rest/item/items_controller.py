from flask_restful import Resource
from flask import Response, request
import json
from . import items_service
from flask_jwt_extended import jwt_required
from wrappers import project_access

FIELDS_TO_EXCLUDE = ['id','created']

class ItemsByProjectApi(Resource):
    def get(self, project_id, model):
        response, mimetype, status = items_service.get_items_by_project(project_id, model, request.args)
        return Response(response, mimetype=mimetype, status=status)
    
    @jwt_required()
    @project_access.project_access_required()
    def post(self, project_id, model):
        data = request.json if request.is_json else request.form
        messages, status = items_service.create_item(project_id,model, data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class ItemByProjectApi(Resource):

    def get(self, project_id, model, item_id):
        item = items_service.get_item(project_id, model, item_id)
        return Response(item, mimetype="application/json", status=200)

    @jwt_required()
    @project_access.project_access_required()
    def put(self, project_id, model, item_id):
        data = request.json if request.is_json else request.form
        messages, status = items_service.update_item(project_id,model, item_id, data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
    
    @jwt_required()
    @project_access.project_access_required()
    def delete(self, project_id,model, item_id):
        messages, status = items_service.delete_item(project_id,model,item_id)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class ModelByProjectStatsApi(Resource):
    def get(self, project_id, model, field):
        
        stats = items_service.get_model_field_stats(project_id, model, field)
        return Response(json.dumps(stats), mimetype="application/json", status=200)
