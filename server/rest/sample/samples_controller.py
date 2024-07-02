from flask_restful import Resource
from flask import Response, request
import json
from . import samples_service

class SamplesApi(Resource):
    def get(self):
        response, mimetype, status = samples_service.get_samples(request.args)
        return Response(response, mimetype=mimetype, status=status)
        
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        messages, status = samples_service.create_sample(project_id,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
    
class SampleByProjectApi(Resource):
    def get(self, project_id, sample_id):
        sample = samples_service.get_samples_by_project(project_id,sample_id)
        return Response(sample.to_json(), mimetype="application/json", status=200)
    
    def put(self, project_id,sample_id):
        data = request.json if request.is_json else request.form
        messages, status = samples_service.update_sample(project_id,sample_id,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
    
    def delete(self, project_id, sample_id):
        messages, status = samples_service.delete_sample(project_id,sample_id)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class SamplesByProjectApi(Resource):
    def get(self, project_id):
        response, mimetype, status = samples_service.get_samples(project_id, request.args)
        return Response(response, mimetype=mimetype, status=status)
        
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        messages, status = samples_service.create_sample(project_id,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)


class SamplesByProjectUploadApi(Resource):
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        messages, status = samples_service.upload_samples(project_id,request.files,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)