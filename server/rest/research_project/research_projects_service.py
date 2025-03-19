from db.models import ResearchProject,ResearchModel
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import NotFound,Conflict,BadRequest
from helpers import schema

def get_project(project_id):
    project = ResearchProject.objects(project_id=project_id).first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")
    return project

def get_projects(offset=0,limit=20,
                filter=None,sort_order=None):
    limit=int(limit)
    offset=int(offset)
    projects = ResearchProject.objects().exclude('id')
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
    models = ResearchModel.objects(project_id=project_id).exclude('id', 'created').as_pymongo()
    return dict(
        name=project.name,
        version=project.version,
        description=project.description,
        models=list(models)
    )

def create_project(data, format):
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
    project_id = project_to_save.project_id

    existing_project = ResearchProject.objects(project_id=project_id).first()
    if existing_project:
        raise Conflict(description=f"Project: {project_id} already exists")
        
    models = [ResearchModel(project_id=project_id, **model) for model in schema_models]
    try:
        ResearchModel.objects.insert(models)
    except Exception as error:
        raise BadRequest(description=f"Error saving the research models: {error}")

    project_to_save.models = [model.get('name') for model in schema_models]

    project_to_save.save()
    return f"Project {project_to_save.project_id} correctly saved"

def convert_id_fields_to_required(data):
    for model in data.get('models', []):
        for id_field in model.get('id_format'):
            for attr in model.get('fields'):
                if attr['key'] == id_field:
                    attr['required'] = True
