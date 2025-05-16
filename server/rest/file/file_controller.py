from flask_restful import Resource
from . import file_service

class FileAPI(Resource):
    def get(self, hash):
        return file_service.download_protocol(hash)

class ProjectFilesAPI(Resource):
    def get(self, project_id, model_name):
        return file_service.download_project_model_files(project_id, model_name)
