from db.models import ResearchProject,ResearchModel
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import NotFound,Conflict,BadRequest
from helpers import schema, user as user_helper
from ..audit.audit_service import create_audit_log
from db.enums import Actions, DocumentTypes

def get_project(project_id):
    project = ResearchProject.objects(project_id=project_id).first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")
    return project

def archive_project(project_id):
    project = get_project(project_id)
    user = user_helper.get_current_user()
    
    # Store previous state for audit log
    previous_state = project.to_dict()
    
    project.modify(archived=True)
    
    # Create audit log
    create_audit_log(
        user=user.name,
        action=Actions.ARCHIVE,
        document_type=DocumentTypes.PROJECT,
        document_id=project_id,
        project_id=project_id,
        previous_object=previous_state,
        new_object=project.to_mongo().to_dict()
    )
    
    return {'message': f'Project {project_id} archived'}

def unarchive_project(project_id):
    project = get_project(project_id)
    user = user_helper.get_current_user()
    
    # Store previous state for audit log
    previous_state = project.to_mongo().to_dict()
    
    project.modify(archived=False)
    
    # Create audit log
    create_audit_log(
        user=user.name,
        action=Actions.UNARCHIVE,
        document_type=DocumentTypes.PROJECT,
        document_id=project_id,
        project_id=project_id,
        previous_state=previous_state,
        new_object=project.to_mongo().to_dict()
    )
    
    return {'message': f'Project {project_id} activated'}

def get_projects(offset=0,limit=20,
                filter=None,sort_order=None, archived=None):
    archived = True if archived and archived == 'true' else False    
    projects = ResearchProject.objects(archived=archived).exclude('id')
    if filter:
        projects= projects.filter((Q(name__icontains=filter) | Q(name__iexact=filter)))
    if sort_order:
        sort_column = "name"
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        projects = projects.order_by(sort)
    return projects.count(), list(projects.skip(offset).limit(limit).as_pymongo())

def get_project_schema(project_id):
    project = ResearchProject.objects(project_id=project_id).exclude('id','created').first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")
    models = ResearchModel.objects(project_id=project_id).exclude('id','created','created_by').as_pymongo()
    return dict(
        name=project.name,
        version=project.version,
        description=project.description,
        models=list(models)
    )

def create_project(data, format):
    user = user_helper.get_current_user()
    name = data.get('name')
    version = data.get('version')
    if not all([name,version]):
        raise BadRequest(description=f"name and version are required")
    project_id = f"{name}_{version}"
    
    content = data
    if format == 'yaml':
        content, error = schema.validate_yaml(content)
        if error:
            return error, 400
    errors = schema.validate_research_project_schema(content)
    if errors:
        raise BadRequest(description=f"{'; '.join(errors)}")
    ##CHANGE ID FIELDS TO REQUIRED
    convert_id_fields_to_required(content) 

    #pop out models
    schema_models = content.pop('models', [])

    project_to_save = ResearchProject(**content)
    project_to_save.project_id = project_id
    project_to_save.created_by = user.name

    existing_project = ResearchProject.objects(project_id=project_id).first()
    if existing_project:
        raise Conflict(description=f"Project: {project_id} already exists")
        
    models = [ResearchModel(project_id=project_id, created_by=user.name,**model) for model in schema_models]
    try:
        ResearchModel.objects.insert(models)
    except Exception as error:
        raise BadRequest(description=f"Error saving the research models: {error}")

    project_to_save.models = [model.get('name') for model in schema_models]

    project_to_save.save()
    
    # Create audit log for project creation
    create_audit_log(
        user=user.name,
        action=Actions.CREATE,
        document_type=DocumentTypes.PROJECT,
        document_id=project_id,
        project_id=project_id,
        new_object=project_to_save.to_mongo().to_dict(),
        metadata={'created_models': [model.get('name') for model in schema_models]}
    )
    
    # Create audit logs for each model creation
    for model in models:
        create_audit_log(
            user=user.name,
            action=Actions.CREATE,
            document_type=DocumentTypes.MODEL,
            document_id=model.name,
            project_id=project_id,
            new_object=model.to_mongo().to_dict()
        )

    user.modify(push__projects=project_id)
    return f"Project {project_to_save.project_id} correctly saved"

def convert_id_fields_to_required(data):
    for model in data.get('models', []):
        for id_field in model.get('id_format'):
            for attr in model.get('fields'):
                if attr['key'] == id_field:
                    attr['required'] = True

