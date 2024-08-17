
from flask_restful import Resource
from flask import Response
from . import stats_service
import json

class LookupApi(Resource):
    def get(self):
        response = stats_service.lookup_data()
        return Response(json.dumps(response), mimetype="application/json", status=200)
        
class ModelStatsApi(Resource):
    def get(self, model, field):
        response = stats_service.get_model_stats(model, field)
        return Response(json.dumps(response), mimetype="application/json", status=200)
        