from db.models import AuditLog
from db.enums import Actions, DocumentTypes
from helpers import data
from datetime import datetime
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import BadRequest

def get_audit_logs(args):
    try:
        query_args = dict(**args)
        document_id = query_args.pop('document_id', None)
        limit, offset = data.get_pagination(query_args)
        sort_column, sort_order = data.get_sort(query_args)

        q_query = None
        if document_id:
            q_query = (Q(document_id__icontains=document_id) | Q(document_id__iexact=document_id))

        logs = AuditLog.objects(**query_args)
        
        if q_query:
            logs = logs.filter(q_query)

        if sort_column and sort_order:
            sort = '-' + sort_column if sort_order == 'desc' else sort_column
            logs = logs.order_by(sort)

        total = logs.count()
        response = dict(total=total, data=list(logs.skip(offset).limit(limit).as_pymongo()))
        return data.dump_json(response), "application/json"

    except Exception as e:
        print(e)
        raise BadRequest(description=str(e))

def get_project_audit_logs(project_id, args):
    # Create a mutable copy of args
    query_args = dict(args)
    query_args['project_id'] = project_id
    return get_audit_logs(query_args)

def get_document_audit_logs(document_type, document_id, args):
    # Create a mutable copy of args
    query_args = dict(args)
    query_args['document_type'] = document_type
    query_args['document_id'] = document_id
    return get_audit_logs(query_args)

def create_audit_log(user: str, action: Actions, document_type: DocumentTypes, 
                    document_id: str, project_id: str, previous_object: dict = None, 
                    new_object: dict = None, changes: dict = None, metadata: dict = None):
    """
    Create an audit log entry for a document operation.
    
    Args:
        user: The user performing the action
        action: The type of action (CREATE, UPDATE, DELETE, etc.)
        document_type: The type of document being modified
        document_id: The ID of the document
        project_id: The project context
        previous_object: The previous state of the document (for updates/deletes)
        new_object: The new state of the document (for creates/updates)
        changes: Specific changes made (for updates)
        metadata: Additional context about the operation
    """
    audit_log = AuditLog(
        user=user,
        action=action,
        document_type=document_type,
        document_id=document_id,
        project_id=project_id,
        previous_object=previous_object,
        new_object=new_object,
        changes=changes,
        metadata=metadata,
        timestamp=datetime.now()
    )
    audit_log.save()
    return audit_log 