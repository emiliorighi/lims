from db.models import ResearchModel, ResearchProject,ResearchItem,FileLink,File
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import NotFound,Conflict,BadRequest
from ..links import link_service
from helpers import schema, data as data_helper, user as user_helper
from ..audit.audit_service import create_audit_log
from db.enums import Actions, DocumentTypes

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

def get_records_count_of_related_models(project_id, model_name):
    get_project_model(project_id, model_name)
    related_models = ResearchModel.objects(reference_model=model_name).scalar('name')
    counts = dict()
    for related_model in related_models:
        counts[related_model] = ResearchItem.objects(project_id=project_id, model_name=related_model).count()
    return counts

def update_field_description(project_id, model_name, field_key, payload):
    user = user_helper.get_current_user()
    model = get_project_model(project_id, model_name)

    field = next((f for f in model.fields if f.key == field_key), None)
    if field:
        raise NotFound(description=f"{field_key} is not present in {model_name}")
    previous_state = model.to_mongo().to_dict()
    field['description'] = payload.get('description')
    model.save()
    model.reload()
    create_audit_log(
        user=user.name,
        action=Actions.UPDATE,
        document_type=DocumentTypes.MODEL,
        document_id=model_name,
        project_id=project_id,
        previous_object=previous_state,
        new_object=model.to_mongo().to_dict(),
        changes={'description': payload.get('description')}
    )
    return f"{field_key} description successfully updated"


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
    if not name:
        raise BadRequest(description=f"Name is mandatory")
    
    name = name.strip()
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
    
    data['id_format'] = [id_field.strip() for id_field in data.get('id_format')] #strip values
    id_format_fields = data.get('id_format')

    for field in data.get('fields'):
        field['key'] = field.get('key').strip() #strip keys

        #set id fields to required
        if field.get('key') in id_format_fields:
            field['required'] = True

    model_to_save = ResearchModel(project_id=project_id,created_by=user.name, **data)
    try:
        model_to_save.save()
        # Create audit log
        create_audit_log(
            user=user.name,
            action=Actions.CREATE,
            document_type=DocumentTypes.MODEL,
            document_id=name,
            project_id=project_id,
            new_object=model_to_save.to_mongo().to_dict()
        )
    except Exception as error:
        raise BadRequest(description=f"Error saving the research model: {error}")

def delete_model(project_id, model_name):
    model = get_project_model(project_id, model_name)
    user = user_helper.get_current_user()
    
    # Store model data for audit log
    model_data = model.to_mongo().to_dict()
    
    ##delete ref_models and related data
    delete_model_related_data(project_id, model_name)
    
    ref_models = ResearchModel.objects(project_id=project_id,reference_model=model_name)
    ref_models_names = []
    for ref_model in ref_models:
        name = ref_model.name
        ref_models_names.append(name)
        delete_model_related_data(project_id, name)
        create_audit_log(
            user=user.name,
            action=Actions.DELETE,
            document_type=DocumentTypes.MODEL,
            previous_object=ref_model.to_mongo().to_dict(),
            document_id=name,
            project_id=project_id,
        )

    ref_models.delete()
    model.delete()
    
    # Create audit log
    create_audit_log(
        user=user.name,
        action=Actions.DELETE,
        document_type=DocumentTypes.MODEL,
        document_id=model_name,
        project_id=project_id,
        previous_object=model_data,
        metadata={'deleted_reference_models': ref_models_names}
    )
    
    return dict(message=f"{model_name} deleted, related models {' ,'.join(ref_models_names)}")

def delete_model_related_data(project_id, model_name):
    user = user_helper.get_current_user()
    query=data_helper.project_model_query(project_id, model_name)
    links = FileLink.objects(**query)
    for link in links:
        create_audit_log(
            user=user.name,
            action=Actions.DELETE,
            document_type=DocumentTypes.FILE_LINK,
            document_id=link.hash,
            project_id=project_id,
            previous_object=link.to_mongo().to_dict()
        )   
    hashes = links.scalar('hash')
    
    links.delete()
    files = File.objects(hash__in=list(hashes))
    for file in files:
        link_service.delete_unbound_file(file.hash)

    items = ResearchItem.objects(**query)
    for item in items:
        create_audit_log(
            user=user.name,
            action=Actions.DELETE,
            document_type=DocumentTypes.RECORD,
            document_id=item.item_id,
            project_id=project_id,
            previous_object=item.to_mongo().to_dict()
        )
    items.delete()

def update_model(project_id, model_name, data):
    """
    Update a research model and handle reference model name updates
    """
    user = user_helper.get_current_user()
    model = get_project_model(project_id, model_name)
    
    # Store previous state for audit log
    previous_state = model.to_mongo().to_dict()
    
    new_name = data.get('name', '').strip() if data.get('name') else None

    # If name is being updated, check for conflicts
    if new_name and new_name != model_name:
        existing_model = ResearchModel.objects(project_id=project_id, name=new_name).first()
        if existing_model:
            raise Conflict(description=f"A model with name {new_name} already exists for project {project_id}")

    # Validate reference model if provided
    ref_model = data.get('reference_model')
    if ref_model:
        reference_model = ResearchModel.objects(project_id=project_id, name=ref_model).first()
        if not reference_model:
            raise BadRequest(description=f"The reference model {ref_model} does not exist in {project_id}")

    # Validate schema if fields are being updated
    if 'fields' in data or 'id_format' in data:
        errors = schema.validate_model(data)
        if errors:
            raise BadRequest(description=f"{'; '.join(errors)}")

        # Process id_format if provided
        if 'id_format' in data:
            data['id_format'] = [id_field.strip() for id_field in data.get('id_format')]
            id_format_fields = data.get('id_format')

        # Process fields if provided
        if 'fields' in data:
            for field in data.get('fields'):
                field['key'] = field.get('key').strip()
                if 'id_format' in data and field.get('key') in id_format_fields:
                    field['required'] = True

    # Update the model with new data
    for key, value in data.items():
        if hasattr(model, key):
            setattr(model, key, value)
        
    try:
        model.save()
        ResearchItem.objects(project_id=project_id, model_name=model_name).update(set__model_name=new_name)
        # If name was updated, update all models that reference this one
        if new_name and new_name != model_name:
            ResearchModel.objects(
                project_id=project_id,
                reference_model=model_name
            ).update(
                set__reference_model=new_name,
            )
        
        # Create audit log
        create_audit_log(
            user=user.name,
            action=Actions.UPDATE,
            document_type=DocumentTypes.MODEL,
            document_id=new_name or model_name,
            project_id=project_id,
            previous_object=previous_state,
            new_object=model.to_mongo().to_dict(),
            changes=data
        )
        
        return {'message': f'{model_name} updated successfully'}
    except Exception as error:
        raise BadRequest(description=f"Error updating the research model: {error}")
