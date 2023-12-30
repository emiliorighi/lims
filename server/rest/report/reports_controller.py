from flask import Response,request
from flask_restful import Resource
from . import reports_service
from flask_jwt_extended import jwt_required
import json


class ReportsApi(Resource):

    def get(self):
        return []
    
    def post(self):
        return

class ReportApi(Resource):

    #download goat_report
    def get(self, id):
        tsv_goat_report = reports_service.download_goat_report()
        mimetype="text/tab-separated-values"
        encode='utf-8'            
        return Response(tsv_goat_report.encode(encode), mimetype=mimetype, headers={"Content-disposition": f"attachment; filename={file_name}"})

    @jwt_required()
    def post(self):
        goat_report = request.files.get('goat_report')
        saved_species, errors = reports_service.upload_goat_report(goat_report)
        response = dict(saved_species=saved_species,errors=errors)
        return Response(json.dumps(response), mimetype="application/json", status=200)