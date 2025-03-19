from db.models import ResearchItem,ResearchModel,ResearchProject
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from mongoengine.queryset.visitor import Q
from helpers import data,filter,schema
from ..research_project import research_projects_service
from ..research_models import model_service

def check_project_exists(project_id):
    if not ResearchProject.objects(project_id=project_id).first():
        raise NotFound(description=f"{project_id} not found")


def get_model(project_id, model_name):
    model = ResearchModel.objects(project_id=project_id, name= model_name).first()
    if not model:
        raise NotFound(description=f"Model {model_name} not found for project {project_id}")
    return model


def get_items(args):
    try:
        
        filter = args.pop('filter', None)

        q_query = None
        
        if filter:
            q_query =(Q(item_id__icontains=filter) | Q(item_id__iexact=filter))

        limit, offset = data.get_pagination(args)     

        sort_column, sort_order = data.get_sort(args)
        
        format = args.pop('format', 'json')
        
        selected_fields = args.pop('fields', None)
        
        query, q_query = data.create_query(args, q_query)
        items = ResearchItem.objects(**query)
        if q_query:
            items = items.filter(q_query)

        if sort_column and sort_order:
            sort = '-' + sort_column if sort_order == 'desc' else sort_column
            items = items.order_by(sort)

        if selected_fields:
            selected_fields = selected_fields.split(',')
            items = items.only(*selected_fields)

        fields = selected_fields if selected_fields else ['project_id', 'model_name', 'item_id', 'reference_id']
        return data.generate_response(format, fields, items, limit, offset)

    except Exception as e:
        print(e)
        raise BadRequest(description=f"{e}")

def get_item(project_id, model_name, item_id):
    item = ResearchItem.objects(project_id=project_id, model_name=model_name, item_id=item_id).first()
    return item

def create_item(project_id, model_name, data):
    check_project_exists(project_id)
    model = get_model(project_id, model_name)
    id_fields = model.id_format

    item_id = schema.create_item_id(id_fields, data)
    ## check if item already exists in the project and model context
    existing_item = get_item(project_id, model_name, item_id)
    if existing_item:
        raise Conflict(description=f"An Item with id: {item_id} already exists in {model_name} of project {project_id}")

    missing_fields = schema.validate_required_fields(model, data)
    if missing_fields:
        raise BadRequest(description=f"{', '.join(missing_fields)} is/are mandatory")

    if model.reference_model:
        ## check reference id field and related record exist
        reference_id = data.get('reference_id')
        if not reference_id:
            raise BadRequest(description=f"reference_id field is mandatory and must point to an item_id of {model.referce_model}")
        ref_item = get_item(project_id, model.reference_model, reference_id)
        if not ref_item:
            raise NotFound(description=f"Reference item with id: {reference_id} not found. Create it first before referencing to it")    
    # Evaluate the fields and raise an error if there are any issues
    evaluation_errors = filter.evaluate_model_fields(model.fields, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
        # Helper function to handle shared logic

    item_to_save={
        "item_id":item_id,
        "model_name":model_name,
        "project_id":project_id,
        **data
    }

    try: 
        ResearchItem(**item_to_save).save()

    except Exception as e:
        raise BadRequest(description=e)
    
    return f"{model_name} {item_id} of {project_id} correctly saved!" # Return the created sample with 201 Created status


def update_item(project_id, model_name, item_id, data):

    check_project_exists(project_id)

    model = get_model(project_id, model_name)

    item = ResearchItem.objects(project_id=project_id, model_name=model_name, item_id=item_id).first()
    if not item:
        raise NotFound(description=f"{model_name}: {item_id} not found")
    
    new_item_id = schema.create_item_id(model.id_format, data)
    
    if new_item_id and item_id != new_item_id:
        message = f"{model_name} {item_id} has changed into {new_item_id}, the value of the fields {','.join(model.id_fields)} can't be changed"
        raise BadRequest(description=message)
    
    evaluation_errors = filter.evaluate_model_fields(model.fields, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    
    item.update(**data)
    return f"{model}: {item_id} successfully updated"



def delete_item(project_id, model_name, item_id):
    item_to_delete = ResearchItem.objects(project_id=project_id, model_name=model_name, item_id=item_id).first()
    if not item_to_delete:
        raise NotFound(description=f"Item {item_id} in {model_name} of {project_id}, not found")
    ##delete related records too
    ResearchItem.objects(project_id=project_id, reference_id=item_id).delete()

    item_to_delete.delete()

    return f"{model_name}: {item_id} successfully deleted"

#TODO: ADD QUERY
def get_model_field_stats(project_id, model_name, field):

    #check if project exists
    research_projects_service.get_project(project_id)

    #retrieve db model
    pipeline = [
            {
                "$project": {
                    "field_value": {
                        "$ifNull": [f"${field}", "No Value"]
                    }
                }
            },
            {"$unwind": "$field_value"},
            {
                "$group": {
                    "_id": "$field_value",
                    "count": {"$sum": 1}
                }
            },
        ]
    response = {
        doc["_id"]: doc["count"]
        for doc in ResearchItem.objects(project=project_id, model_name=model_name).aggregate(pipeline)
    }
    return response
