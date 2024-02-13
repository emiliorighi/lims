from db.models import Project,ProjectDraft
from errors import NotFound
from mongoengine.queryset.visitor import Q
from jsonschema import validators
import json,yaml,requests
from ..utils import utils

model = Project
JSON_SCHEMA_PATH='/server/project-spec.json'

def get_project(id):
    return utils.return_document_by_id(model, dict(project_id=id), ('id','created'))

def get_projects(offset=0,limit=20,
                filter=None,sort_order=None):
    if filter:
        projects= model.objects((Q(name__icontains=filter) | Q(name__iexact=filter))).exclude('id','created')
    else:
        projects = model.objects().exclude('id','created')
    if sort_order:
        sort_column = "name"
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        projects = projects.order_by(sort)
    return projects.count(), projects[int(offset):int(offset)+int(limit)]

def create_project(data):
    errors = []
    jsonschema_errors=jsonschema_validation(data)
    errors.extend(jsonschema_errors)
    if errors:
        return errors, 401
    for m in ['sample','experiment']:
        errors.extend(validate_model(data.get(m)))
    if errors:
        return errors, 401
    project_to_save = Project(**data)
    project_draft = ProjectDraft.objects(project_id=project_to_save.project_id)
    if project_draft.first():
        project_draft.delete()
    project_to_save.save()
    return [dict(message=f"Project {project_to_save.project_id} correctly saved")], 201

# def create_project(format='json',url=None,schema=None):
#     try:
#         if url:
#             response = requests.get(url)
#             schema = response.content
#         if not schema:
#             return ['schema not found'], 401
#         format = format.lower()
#         project=schema
#         if format == 'yaml':
#             project = yaml.load(schema, yaml.SafeLoader)
#             project['version'] = str(project['version'])
        
#         errors = []
#         jsonschema_errors=jsonschema_validation(project)
#         errors.extend(jsonschema_errors)
#         for m in ['sample','experiment']:
#             errors.extend(validate_model(project[m]))
#         if len(errors):
#             print(errors)
#             return errors, 401
        
#         project_to_save = Project(**project)
#         project_to_save.save()
#         return project_to_save.as_pymongo(), 201
    
#     except Exception as e:
#         return [e], 401

def validate_model(model):
    errors = []
    for id_field in model.get('id_format'):
        if not any(id_field == f['key'] for f in model['fields']):
            errors.append(f"{id_field} not found")
        
    return errors

def jsonschema_validation(project):
    print(project)
    errors_collection = []
    with open(JSON_SCHEMA_PATH, 'r') as file:
        data = json.load(file)        
        v = validators.Draft202012Validator(data)
        errors = v.iter_errors(project)
        for error in errors:
            errors_collection.append(dict(message=error.message ,path=error.json_path))
    return errors_collection

# def update_draft_project(id):
#     draft_project = 

# def download_yaml_schema(project):

# def upload_yaml_schema(payload, file=None):