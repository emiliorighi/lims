from flask_restful import Resource
from flask import Response, request
import json
from . import records_service
from flask_jwt_extended import jwt_required
from wrappers import project_access

FIELDS_TO_EXCLUDE = ['id','created']

class ItemsApi(Resource):
    @jwt_required()
    def get(self):
        response, mimetype = records_service.get_items(request.args)
        return Response(response, mimetype=mimetype, status=200)

class ItemsByProjectModelApi(Resource):
    @jwt_required()
    def get(self, project_id, model_name):
        args = dict(project_id=project_id, model_name=model_name,**request.args)
        response, mimetype = records_service.get_items(args)
        return Response(response, mimetype=mimetype, status=200)
    
    @jwt_required()
    @project_access.project_access_required()
    def post(self, project_id, model_name):
        data = request.json if request.is_json else request.form
        messages = records_service.create_item(project_id, model_name, data)
        return Response(json.dumps(messages), mimetype="application/json", status=201)
    
class RelatedItemsByProjectModelApi(Resource):
    @jwt_required()
    def get(self, project_id, model_name, record_id):
        args = dict(project_id=project_id, reference_id=record_id, **request.args)
        response, mimetype = records_service.get_items(args)
        return Response(response, mimetype=mimetype, status=200)
    
    @jwt_required()
    @project_access.project_access_required()
    def post(self, project_id, model_name):
        data = request.json if request.is_json else request.form
        messages = records_service.create_item(project_id, model_name, data)
        return Response(json.dumps(messages), mimetype="application/json", status=201)
    

class ItemByProjectModelApi(Resource):

    @jwt_required()
    def get(self, project_id, model_name, record_id):
        item = records_service.get_item(project_id, model_name, record_id)
        return Response(item.to_json(), mimetype="application/json", status=200)

    @jwt_required()
    @project_access.project_access_required()
    def put(self, project_id, model_name, record_id):
        data = request.json if request.is_json else request.form
        message = records_service.update_item(project_id,model_name, record_id, data)
        return Response(json.dumps(message), mimetype="application/json", status=201)
    
    @jwt_required()
    @project_access.project_access_required()
    def delete(self, project_id,model_name, record_id):
        message = records_service.delete_item(project_id,model_name,record_id)
        return Response(json.dumps(message), mimetype="application/json", status=201)



class ModelByProjectStatsApi(Resource):
    def get(self, project_id, model, field):
        stats = records_service.get_model_field_stats(project_id, model, field)
        return Response(json.dumps(stats), mimetype="application/json", status=200)
