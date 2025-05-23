import json
from flask_restful import Resource
from flask import Response
from . import lookup_service

class LookupProjectDataApi(Resource):
    def get(self, project_id):
        resp = lookup_service.lookup_project_related_data(project_id)
        return Response(json.dumps(resp), mimetype="application/json", status=200)

class LookupModelDataApi(Resource):
    def get(self, project_id, model_name):
        resp = lookup_service.lookup_model_related_data(project_id, model_name)
        return Response(json.dumps(resp), mimetype="application/json", status=200)
  