from flask_restful import Resource
from . import file_service

class FileAPI(Resource):
    def get(self, hash):
        return file_service.download_protocol(hash)
