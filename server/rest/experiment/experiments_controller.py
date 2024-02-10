from flask_restful import Resource
from flask import Response, request
import json
from db.models import Experiment
from . import experiments_service
from errors import NotFound
from flask_jwt_extended import jwt_required


FIELDS_TO_EXCLUDE = ['id','created']

class ExperimentsApi(Resource):
    def get(self, project_id):
        return
        
    def post(self, project_id):
        return

class ExperimentApi(Resource):
    def get(self, project_id, sample_id):
        return
    
    def put(self, project_id,sample_id):
        
        return
    def delete(self, project_id, sample_id):

        return

# ##post request to handle large list of assemblies/experiments/local_samples/biosamples/annotations ids
# class ExperimentsApi(Resource):

#     def get(self):
#         total,data = experiments_service.get_reads(**request.args)
#         json_resp = dict(total=total,data=list(data.as_pymongo()))
#         return Response(json.dumps(json_resp), mimetype="application/json", status=200)

# ##post request to handle large list of assemblies/experiments/local_samples/biosamples/annotations ids
# class ExperimentApi(Resource):

#     def get(self,accession=None):
#         experiment_obj = Experiment.objects(experiment_accession=accession).first()
#         if not experiment_obj:
#             raise NotFound
#         return Response(experiment_obj.to_json(), mimetype="application/json", status=200)

#     @jwt_required()
#     def post(self,accession):
#         response = experiments_service.create_read_from_experiment_accession(accession)
#         return Response(json.dumps(response['message']), mimetype="application/json", status=response['status'])

#     @jwt_required()
#     def delete(self,accession):
#         deleted_accession = experiments_service.delete_experiment(accession)
#         return Response(json.dumps(deleted_accession), mimetype="application/json", status=201)

# class ExperimentRelatedAnalysis(Resource):
#     def get(self,id):
#         return