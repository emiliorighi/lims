from flask_restful import Resource
from flask import Response, request
import json
from . import experiments_service


FIELDS_TO_EXCLUDE = ['id','created']

class ExperimentsApi(Resource):
    def get(self):
        response, mimetype, status = experiments_service.get_experiments(request.args)
        return Response(response, mimetype=mimetype, status=status)
    
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        messages, status = experiments_service.create_experiment(project_id,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class ExperimentsByProjectApi(Resource):
    def get(self, project_id):
        response, mimetype, status = experiments_service.get_experiments_by_project(project_id, request.args)
        return Response(response, mimetype=mimetype, status=status)
    
    def post(self, project_id):
        data = request.json if request.is_json else request.form
        messages, status = experiments_service.create_experiment(project_id,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class ExperimentByProjectApi(Resource):
    def get(self, project_id, experiment_id):
        sample = experiments_service.get_experiment(project_id, experiment_id)
        return Response(json.dumps(sample), mimetype="application/json", status=200)
    
    def put(self, project_id,experiment_id):
        data = request.json if request.is_json else request.form
        messages, status = experiments_service.update_experiment(project_id,experiment_id,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
    
    def delete(self, project_id, experiment_id):
        messages, status = experiments_service.delete_experiment(project_id,experiment_id)
        return Response(json.dumps(messages), mimetype="application/json", status=status)

class ExperimentsBySampleApi(Resource):
    def get(self, project_id, sample_id):
        total, data = experiments_service.get_experiments(project_id,sample_id,**request.args)
        json_resp = dict(total=total,data=list(data.as_pymongo()))
        return Response(json.dumps(json_resp), mimetype="application/json", status=200)
    
    def post(self, project_id, sample_id): 
        data = request.json if request.is_json else request.form
        messages, status = experiments_service.create_experiment(project_id,sample_id,data)
        return Response(json.dumps(messages), mimetype="application/json", status=status)
    
    ## TODO: Add update and delete all experiments related to one sample?
    # def put():
    # def delete():