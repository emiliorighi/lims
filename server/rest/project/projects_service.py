from db.models import Project,ProjectDraft
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import  NotFound
from helpers import schema


JSON_SCHEMA_PATH='/server/project-spec.json'

def get_project(project_id):
    project = Project.objects(project_id=project_id).exclude('id').first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")
    return project

def get_projects(offset=0,limit=20,
                filter=None,sort_order=None):
    limit=int(limit)
    offset=int(offset)
    if filter:
        projects= Project.objects((Q(name__icontains=filter) | Q(name__iexact=filter))).exclude('id','created')
    else:
        projects = Project.objects().exclude('id','created')
    if sort_order:
        sort_column = "name"
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        projects = projects.order_by(sort)
    return projects.count(), list(projects.skip(offset).limit(limit).as_pymongo())

def create_project(data):
    errors = schema.validate_content(data)

    if errors:
        return errors, 401
    
    convert_to_required(data)     ##CHANGE ID FIELDS TO REQUIRED


    project_to_save = Project(**data)
    
    existing_project = Project.objects(project_id=project_to_save.project_id).first()
    if existing_project:
        return [f"Project: {project_to_save.project_id} already exists"], 401
    
    project_draft = ProjectDraft.objects(project_id=project_to_save.project_id).first()
    if project_draft:
        project_draft.delete()

    project_to_save.save()
    return [f"Project {project_to_save.project_id} correctly saved"], 201

def convert_to_required(data):
    for m in ['sample','experiment']:
        model = data.get(m)
        for id_field in model.get('id_format'):
            for attr in model.get('fields'):
                if attr['key'] == id_field:
                    attr['required'] = True

def validate_project(data, format='json'):

    content = data
    if format == 'yaml':
        content, error = schema.validate_yaml(data)
        if error:
            return error, 400
    errors = schema.validate_content(content)

    if errors:
        return errors, 400
    else:
        return [f"Project {content.get('project_id')} is valid!"], 200
    