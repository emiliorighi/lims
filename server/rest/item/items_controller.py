from flask_restful import Resource
from flask import Response, request
import json
from . import items_service


FIELDS_TO_EXCLUDE = ['id','created']

class ItemsByProjectApi(Resource):
    def get(self, project_id, model):
        response, mimetype, status = items_service.get_items_by_project(project_id, model, request.args)
        return Response(response, mimetype=mimetype, status=status)
    
    def post(self, project_id, model):
        data = request.json if request.is_json else request.form
        messages, status = items_service.create_item(project_id,model, data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class ItemByProjectApi(Resource):

    def get(self, project_id, model, item_id):
        item = items_service.get_item(project_id, model, item_id)
        return Response(item.to_json(), mimetype="application/json", status=200)

    def put(self, project_id,model, item_id):
        data = request.json if request.is_json else request.form
        messages, status = items_service.update_item(project_id,model, item_id, data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
    
    def delete(self, project_id,model, item_id):
        messages, status = items_service.delete_item(project_id,model,item_id)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

# class ModelStatsByProjectApi(Resource):
#     def get(self, project_id, model):
#         exp = items_service.get_experiment(project_id, experiment_id)
#         return Response(exp.to_json(), mimetype="application/json", status=200)

class ModelByProjectStatsApi(Resource):
    def get(self, project_id, model, field):
        
        stats = items_service.get_model_field_stats(project_id, model, field)
        return Response(json.dumps(stats), mimetype="application/json", status=200)
