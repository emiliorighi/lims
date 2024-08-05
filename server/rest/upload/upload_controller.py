import json
from flask_restful import Resource
from flask import Response, request
from . import upload_service

class TsvUploadApi(Resource):
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        message,status = upload_service.upload_tsv(project_id, request.files.get('file'), data)
        return Response(json.dumps(message), mimetype="application/json", status=status)
