from flask_restful import Resource
from flask import Response, request
import json
from . import samples_service

class SamplesApi(Resource):
    def get(self, project_id):
        print(request.args.to_dict(flat=False))
        total, data = samples_service.get_samples(project_id,**request.args)
        json_resp = dict(total=total,data=list(data.as_pymongo()))
        return Response(json.dumps(json_resp), mimetype="application/json", status=200)
        
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        messages, status = samples_service.create_sample(project_id,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class SampleApi(Resource):
    def get(self, project_id, sample_id):
        sample = samples_service.get_sample(project_id,sample_id).as_pymongo()[0]
        return Response(json.dumps(sample), mimetype="application/json", status=200)
    
    def put(self, project_id,sample_id):
        data = request.json if request.is_json else request.form
        messages, status = samples_service.update_sample(project_id,sample_id,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
    
    def delete(self, project_id, sample_id):
        messages, status = samples_service.delete_sample(project_id,sample_id)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class SamplesUploadApi(Resource):
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        messages, status = samples_service.upload_samples(project_id,request.files,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)