
from flask_restful import Resource
from flask import Response
from . import stats_service
import json

class StatsApi(Resource):
    def get(self, model):
        response, status = stats_service.get_stats(model)
        return Response(json.dumps(response), mimetype="application/json", status=status)
        
class ModelStatsApi(Resource):
    def get(self, model, field):
        response = stats_service.get_model_stats(model, field)
        return Response(json.dumps(response), mimetype="application/json", status=200)
        

class ProjectStatsApi(Resource):
    def get(self, project_id, model, field):
        stats = stats_service.get_project_stats(project_id, model, field)
        return Response(json.dumps(stats), mimetype="application/json", status=200)
