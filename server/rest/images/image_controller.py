from flask_restful import Resource
from flask import Response, request
from . import image_service
from helpers import data as data_helper

FIELDS_TO_EXCLUDE = ['id','created']

class ImagesAPI(Resource):
    def get(self, project_id, model, item_id):
        if project_id:
            response, status = image_service.get_protocols_by_project(project_id, request.args)
        else:
            response, status = image_service.get_protocols(request.args)
        return Response(response, mimetype="application/json", status=status)
    
    def post(self, project_id, model, item_id):
        resp, status = image_service.save_protocol(request, project_id)
        return Response(resp, mimetype="application/json", status=status)


class ImageAPI(Resource):
    def get(self, project_id, model, item_id, name):
        protocol = image_service.get_protocol(name)
        return Response(data_helper.dump_json(protocol.to_mongo().to_dict()), mimetype="application/json", status=200)

    def delete(self, project_id, model, item_id, name):
        resp, status = image_service.delete_protocol(name)
        return Response(resp, mimetype="application/json", status=status)

class DownloadProtocolAPI(Resource):
    def get(self, project_id, model, item_id, name):
        return image_service.download_protocol(name)

