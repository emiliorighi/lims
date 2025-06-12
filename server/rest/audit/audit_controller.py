from flask_restful import Resource
from flask import Response, request
from . import audit_service
from flask_jwt_extended import jwt_required
from wrappers import admin

class AuditLogsAPI(Resource):
    @jwt_required()
    @admin.admin_required()
    def get(self):
        response, mimetype = audit_service.get_audit_logs(request.args)
        return Response(response, mimetype=mimetype, status=200)

class ProjectAuditLogsAPI(Resource):
    @jwt_required()
    @admin.admin_required()
    def get(self, project_id):
        response, mimetype = audit_service.get_project_audit_logs(project_id, request.args)
        return Response(response, mimetype=mimetype, status=200)

class DocumentAuditLogsAPI(Resource):
    @jwt_required()
    @admin.admin_required()
    def get(self, document_type, document_id):
        response, mimetype = audit_service.get_document_audit_logs(document_type, document_id, request.args)
        return Response(response, mimetype=mimetype, status=200) 