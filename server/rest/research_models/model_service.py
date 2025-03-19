from db.models import ResearchModel, ResearchProject
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import NotFound,Conflict,BadRequest
from helpers import schema

def get_related_project(project_id):
    project = ResearchProject.objects(project_id=project_id).first()
    if not project:
        raise NotFound(f"Project {project_id} not found!")
    return project

def get_models(project_id, filter=None,  limit=20, offset=0):
    limit=int(limit)
    offset=int(offset)
    models = ResearchModel.objects(project_id=project_id).exclude('id')
    if filter:
        models= models.filter((Q(name__icontains=filter) | Q(name__iexact=filter)))
    return models.count(), list(models.skip(offset).limit(limit).as_pymongo())

def get_model(project_id, name):
    model = ResearchModel.objects(project_id=project_id, name=name).first()
    if not model:
        raise NotFound(description=f"Model {name} for project {project_id} not found")
    return model

def create_model(project_id, data):
    ## create new model
    project = get_related_project(project_id)
    name = data.get('name')
    #check model doesnt exist
    existing_model = ResearchModel.objects(project_id=project_id, name=name).first()
    if existing_model:
        raise Conflict(description=f"A model with name {name} already exists for project {project_id}")

    ref_model = data.get('reference_model')
    if ref_model:
        reference_model = ResearchModel.objects(project_id=project_id, name=ref_model).first()
        if not reference_model:
            raise BadRequest(description=f"The reference model {ref_model} does not exists in {project_id}")
    errors = schema.validate_model_v2(data)
    if errors:
        raise BadRequest(description=f"{'; '.join(errors)}")
    
    #set id fields to required
    id_fields = data.get('id_format')
    for field in data.get('fields'):
        if field.get('key') in id_fields:
            field['required'] = True

    model_to_save = ResearchModel(project_id=project_id, **data)
    try:
        model_to_save.save()
        project.modify(add_to_set__models=name)
    except Exception as error:
        raise BadRequest(description=f"Error saving the research model: {error}")


def update_protocols(project_id, name, protocols):
    project = get_related_project(project_id)

    
def update_links(project_id, name, links):
    project = get_related_project(project_id)
