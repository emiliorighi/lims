from db.models import Experiment,Sample
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from mongoengine.queryset.visitor import Q
from helpers import data,filter,schema
from ..project import projects_service

MODELS={
    "samples": Sample,
    "experiments":Experiment
}

def get_model(model):
    db_model = MODELS.get(model)

    if not db_model:
        raise NotFound(description=f"Model: {model} not found")
    
    return db_model


def get_items_by_project(project_id: str, model: str, args: dict):
    project = projects_service.get_project(project_id)
    db_model = get_model(model)

    limit, offset = data.get_pagination(args)
    sort_column, sort_order = data.get_sort(args)
    response_format = args.get('format', 'json')

    tsv_fields, filters = define_tsv_fields_and_filters(model, project)

    filtered_args = filter_args(args)

    query, q = build_queries(filters, filtered_args)
    query['project'] = project_id
    cursor = db_model.objects(**query).exclude('id')
    if q:
        cursor = cursor.filter(q)

    selected_fields = get_selected_fields(args)
    if selected_fields:
        cursor = cursor.only(*selected_fields)
        tsv_fields.extend(selected_fields)

    if sort_column and sort_order:
        cursor = data.apply_sorting(cursor, sort_column, sort_order)

    return prepare_response(cursor, tsv_fields, response_format, limit, offset)

def define_tsv_fields_and_filters(model, project):
    if model == 'experiments':
        return ['experiment_id', 'sample_id'], project.experiment['fields']
    else:
        return ['sample_id'], project.sample['fields']

def filter_args(args):
    ignored_keys = {"limit", "offset", "sort_order", "sort_column", "format", "fields[]"}
    return {k: v for k, v in args.items() if k not in ignored_keys and v}

def build_queries(filters, filtered_args):
    query = {}
    q = None

    for f in filters:
        key = f.get('key')
        if key not in filtered_args:
            continue
        
        value = filtered_args[key] if filtered_args[key] != 'No Value' else None
        filter_type = f.get('filter')

        if filter_type.get('choices') or filter_type.get('min'):
            query[key] = value
        else:
            condition = Q(**{f"{key}__icontains": value}) | Q(**{f"{key}__iexact": value})
            q = condition if q is None else q & condition

    for key, value in filtered_args.items():
        if any(op in key for op in ['__gte', '__lte', '__gt', '__lt']):
            query[key] = value
        elif key == 'sample_id' or 'experiment_id':
            condition = Q(**{f"{key}__icontains": value}) | Q(**{f"{key}__iexact": value})
            q = condition if q is None else q & condition

    return query, q

def get_selected_fields(args: dict) -> list:
    return [v for k, v in args.items(multi=True) if k.startswith('fields[]')]

def prepare_response(cursor, tsv_fields: list, response_format: str, limit: int, offset: int):
    if response_format == 'tsv':
        return data.generate_tsv(cursor, tsv_fields), "text/tab-separated-values", 200
    
    total = cursor.count()
    response = {'total': total, 'data': list(cursor.skip(offset).limit(limit).as_pymongo())}
    return data.dump_json(response), "application/json", 200


def get_item(project_id, model, item_id):
    db_model = get_model(model)
    query = {"project":project_id}

    if model == 'samples':
        query["sample_id"] = item_id
    else:
        query["experiment_id"] = item_id
    
    item = db_model.objects(**query).exclude('id').first().to_mongo().to_dict()
    if not item:
        raise NotFound(description=f"{item_id} not found")
    return data.dump_json(item)
    
def create_item(project_id, model, data):
    project = projects_service.get_project(project_id)
    # Evaluate the fields and raise an error if there are any issues
    evaluation_errors = filter.evaluate_fields(project, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    
    db_model = get_model(model)
    # Helper function to handle shared logic
    def process_item(project_entity, entity_type, item_key):
        id_fields = project_entity.get('id_format', [])
        item_id = schema.create_item_id(id_fields, data)
        if not item_id:
            raise BadRequest(description=f"Unable to generate {entity_type}_id with the fields provided")

        query = {"project": project_id, item_key: item_id}
        item = db_model.objects(**query).first()

        if item:
            raise Conflict(description=f"{entity_type.capitalize()}: {item_id} already exists!")
        
        missing_fields = schema.validate_required_fields(project_entity, data)
        if missing_fields:
            raise BadRequest(description=f"{', '.join(missing_fields)} is/are mandatory")
    
        item_to_save={
            f"{item_key}":item_id,
            "project":project_id,
            **data
        }

        return item_to_save
    
    # Determine whether we are dealing with samples or experiments
    if model == "samples":
        key = "sample_id"
        item_to_save = process_item(project.sample, "sample", key)
    else:
        key="experiment_id"
        item_to_save = process_item(project.experiment, "experiment", key )

        sample_id = data.get('sample_id')
        if not sample_id:
            raise BadRequest(description="sample_id field is mandatory")

        sample_object = Sample.objects(project=project_id, sample_id=sample_id).first()
        if not sample_object:
            raise BadRequest(description=f"Sample {sample_id} does not exist, create it first")

        item_to_save["sample_id"] = sample_object.sample_id

    try: 
        db_model(
            **item_to_save
        ).save()

    except Exception as e:
        raise BadRequest(description=e)
    
    return f"{model} {key} of {project_id} correctly saved!", 201  # Return the created sample with 201 Created status


def update_item(project_id, model, item_id, data):
    
    project =projects_service.get_project(project_id)
    db_model = get_model(model)
    if model == "samples":
        key = "sample_id"
        id_fields = project.sample.get('id_format', [])

    else:
        key="experiment_id"
        id_fields = project.experiment.get('id_format', [])

    query = {
        f"{key}":item_id,
        "project":project_id
    }
    item = db_model.objects(**query).first()
    if not item:
        raise NotFound(description=f"{key}: {item_id} not found")
    
    new_item_id = schema.create_item_id(id_fields, data)
    
    if new_item_id and item_id != new_item_id:
        message = f"{key} {item_id} has changed into {new_item_id}, the value of the fields {','.join(id_fields)} can't be changed"
        raise BadRequest(description=message)
    
    evaluation_errors = filter.evaluate_fields(project, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    
    item.update(**data)
    return [f"{model}: {item_id} successfully updated"], 201



def delete_item(project_id, model, item_id):
    
    projects_service.get_project(project_id)
    
    db_model = get_model(model)
    if model=='samples':
        key="sample_id"
        experiments = Experiment.objects(project=project_id,sample_id=item_id)
        experiments.delete()
    else:
        key = 'experiment_id'

    query = {
        f"{key}":item_id,
        "project":project_id
    }
    item_to_delete = db_model.objects(**query).first()
    if not item_to_delete:
        raise NotFound(description=f"{key}: {item_id} not found")

    item_to_delete.delete()

    return f"{model}: {item_id} successfully deleted", 201

#TODO: ADD QUERY
def get_model_field_stats(project_id, model, field):

    #check if project exists
    projects_service.get_project(project_id)

    #retrieve db model
    db_model = get_model(model)

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
        for doc in db_model.objects(project=project_id).aggregate(pipeline)
    }
    return response
