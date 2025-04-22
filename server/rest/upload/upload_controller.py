import json
from flask_restful import Resource
from flask import Response, request
from . import upload_service
from flask_jwt_extended import jwt_required
from wrappers import project_access

class TsvUploadApi(Resource):
    @jwt_required()
    @project_access.project_access_required()
    def post(self, project_id, model_name):
        data = request.json if request.is_json else request.form
        message = upload_service.upload_tsv(project_id, model_name, request.files.get('file'), data)
        return Response(json.dumps(message), mimetype="application/json", status=201)
