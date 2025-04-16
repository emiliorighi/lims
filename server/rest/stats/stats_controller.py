
from flask_restful import Resource
from flask import Response, request
from . import stats_service
import json

class LookupApi(Resource):
    def get(self):
        response = stats_service.lookup_data()
        return Response(json.dumps(response), mimetype="application/json", status=200)
        
class ModelStatsApi(Resource):
    def get(self, project_id, model_name, field):
        response = stats_service.get_stats(project_id, model_name,field, request.args)
        return Response(response, mimetype="application/json", status=200)
        
class RecordStatsApi(Resource):
    def get(self, field):
        response = stats_service.get_records_stats(field, request.args)
        return Response(response, mimetype="application/json", status=200)
    
class LinkStatsApi(Resource):
    def get(self, field):
        response = stats_service.get_link_stats(field, request.args)
        return Response(response, mimetype="application/json", status=200)
