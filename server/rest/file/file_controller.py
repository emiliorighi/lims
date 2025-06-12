from flask_restful import Resource
from . import file_service
from flask_jwt_extended import jwt_required

class FileAPI(Resource):
    @jwt_required()
    def get(self, hash):
        return file_service.download_protocol(hash)

class ProjectFilesAPI(Resource):
    @jwt_required()
    def get(self, project_id, model_name, type):
        return file_service.download_project_model_files(project_id, model_name, type)
