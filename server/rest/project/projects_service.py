from db.models import Project
from errors import NotFound
from mongoengine.queryset.visitor import Q
from jsonschema import validators
import json,yaml,requests

def get_project(id):
    project = Project.objects(project_id=id).exclude('id').first()
    if not project:
        raise NotFound
    return project

def get_projects(offset=0,limit=20,
                filter=None,sort_order=None):
    if filter:
        projects= Project.objects((Q(name__icontains=filter) | Q(name__iexact=filter))).exclude('id','created')
    else:
        projects = Project.objects().exclude('id','created')
    if sort_order:
        sort_column = "name"
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        projects = projects.order_by(sort)
    return projects.count(), projects[int(offset):int(offset)+int(limit)]

def validate_project_payload(format='json',url=None,schema=None):
    try:
        if url:
            response = requests.get(url)
            schema = response.content
        if not schema:
            return ['schema not found'], 401
        format = format.lower()
        project=schema
        if format == 'yaml':
            project = yaml.load(schema, yaml.SafeLoader)
            project['version'] = str(project['version'])
        
        errors = []
        jsonschema_errors=jsonschema_validate_project(project)
        errors.extend(jsonschema_errors)
        for m in ['sample','experiment']:
            errors.extend(validate_model(project[m]))
        if len(errors):
            print(errors)
            return errors, 401
        
        project_to_save = Project(**project)
        project_to_save.save()
        return project_to_save.as_pymongo(), 201
    
    except Exception as e:
        return [e], 401

def validate_model(model):
    errors = []
    for id_field in model['id_format']:
        if not any(id_field == f['key'] in f for f in model['fields']):
            errors.append(f"{id_field} not found")
    return errors

def jsonschema_validate_project(project):
    # Specify the path to your JSON file
    json_file_path = '/server/project-spec.json'
    errors_collection = []
    with open(json_file_path, 'r') as file:
        # Load the JSON data
        data = json.load(file)        
        v = validators.Draft202012Validator(data)

        # validate(instance=f, schema=data)
        errors = v.iter_errors(project)
        for error in errors:
            errors_collection.append(dict(message=error.message ,path=error.json_path))
    return errors_collection


# def download_yaml_schema(project):

# def upload_yaml_schema(payload, file=None):