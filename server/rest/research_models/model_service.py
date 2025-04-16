from db.models import ResearchModel, ResearchProject,ResearchItem,FileLink,File
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import NotFound,Conflict,BadRequest
from ..links import link_service
from helpers import schema, data as data_helper, user as user_helper

def get_related_project(project_id):
    project = ResearchProject.objects(project_id=project_id).first()
    if not project:
        raise NotFound(f"Project {project_id} not found!")
    return project

def get_models(args):
    query = {**args}
    limit, offset = data_helper.get_pagination(query)
    sort_column, sort_order = data_helper.get_sort(query)
    format = args.pop('format', 'json')
    selected_fields = args.pop('fields', None)
    q_query = None
    query_set, q_query = data_helper.create_query(query, q_query)
    items = ResearchModel.objects(**query_set)

    if q_query:
        items = items.filter(q_query)

    if sort_column and sort_order:
        sort = '-' + sort_column if sort_order == 'desc' else sort_column
        items = items.order_by(sort)

    if selected_fields:
        selected_fields = selected_fields.split(',')
        items = items.only(*selected_fields)

    fields = selected_fields if selected_fields else ['project_id', 'model_name', 'item_id', 'reference_id']
    return data_helper.generate_response(format, fields, items, limit, offset)


def get_project_models(project_id, filter=None,  limit=20, offset=0):
    limit=int(limit)
    offset=int(offset)
    models = ResearchModel.objects(project_id=project_id).exclude('id')
    if filter:
        models= models.filter((Q(name__icontains=filter) | Q(name__iexact=filter)))
    return models.count(), list(models.skip(offset).limit(limit).as_pymongo())

def get_project_model(project_id, name):
    model = ResearchModel.objects(project_id=project_id, name=name).first()
    if not model:
        raise NotFound(description=f"Model {name} for project {project_id} not found")
    return model

def create_model(project_id, data):
    ## create new model
    user = user_helper.get_current_user()
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
    errors = schema.validate_model(data)
    if errors:
        raise BadRequest(description=f"{'; '.join(errors)}")
    
    #set id fields to required
    id_fields = data.get('id_format')
    for field in data.get('fields'):
        if field.get('key') in id_fields:
            field['required'] = True

    model_to_save = ResearchModel(project_id=project_id,created_by=user.name, **data)
    try:
        model_to_save.save()
        project.modify(add_to_set__models=name)
    except Exception as error:
        raise BadRequest(description=f"Error saving the research model: {error}")

def delete_model(project_id, model_name):
    model = get_project_model(project_id, model_name)
    ##delete ref_models and related data
    delete_model_related_data(project_id, model_name)
    
    ref_models = ResearchModel.objects(project_id=project_id,reference_model=model_name)
    ref_models_names = []
    for ref_model in ref_models:
        name = ref_model.name
        ref_models_names.append(name)
        delete_model_related_data(project_id, name)

    ref_models.delete()
    model.delete()
    return dict(message=f"{model_name} deleted, related models {' ,'.join()}")

def delete_model_related_data(project_id, model_name):
    query=data_helper.project_model_query(project_id, model_name)
    links = FileLink.objects(**query)

    hashes = links.scalar('hash')
    
    links.delete()
    files = File.objects(hash__in=list(hashes))
    for file in files:
        link_service.delete_unbound_file(file.hash)

    ResearchItem.objects(**query).delete()
