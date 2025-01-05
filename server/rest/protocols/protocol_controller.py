from flask_restful import Resource
from flask import Response, request
from . import protocol_service
from helpers import data as data_helper

FIELDS_TO_EXCLUDE = ['id','created']

class ProtocolsAPI(Resource):
    def get(self, project_id=None):
        if project_id:
            response, status = protocol_service.get_protocols_by_project(project_id, request.args)
        else:
            response, status = protocol_service.get_protocols(request.args)
        return Response(response, mimetype="application/json", status=status)
    
    def post(self, project_id=None):
        resp, status = protocol_service.save_protocol(request, project_id)
        return Response(resp, mimetype="application/json", status=status)


class ProtocolAPI(Resource):
    def get(self, name):
        protocol = protocol_service.get_protocol(name)
        return Response(data_helper.dump_json(protocol.to_mongo().to_dict()), mimetype="application/json", status=200)

    def delete(self, name):
        resp, status = protocol_service.delete_protocol(name)
        return Response(resp, mimetype="application/json", status=status)

class DownloadProtocolAPI(Resource):
    def get(self, name):
        return protocol_service.download_protocol(name)

