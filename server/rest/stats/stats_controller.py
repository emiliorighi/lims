
from flask_restful import Resource
from flask import Response, request
from . import stats_service
import json

class StatsApi(Resource):
    def get(self, model):
        response, status = stats_service.get_stats(model)
        return Response(json.dumps(response), mimetype="application/json", status=status)
        
