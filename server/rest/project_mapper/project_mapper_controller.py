import json
from flask_restful import Resource
from flask import Response, request
from . import project_mapper_service


class InferHeaderApi(Resource):
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        messages, status = project_mapper_service.infer_header(project_id, data, request.files)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

