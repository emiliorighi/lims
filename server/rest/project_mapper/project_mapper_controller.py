import json
from flask_restful import Resource
from flask import Response, request
from . import project_mapper_service


##returns the list of mapped attributes
class TsvUploadMapApi(Resource):
    def post(self):
        data = request.json if request.is_json else request.form
        attributes = project_mapper_service.map_attributes_from_tsv(request.files.get('tsv'),data)
        return Response(json.dumps(attributes), mimetype="application/json", status=200)

class InferHeaderApi(Resource):
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        messages, status = project_mapper_service.infer_fields(project_id, data, request.files)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

