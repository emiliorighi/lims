from db.models import Experiment,Sample
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from mongoengine.queryset.visitor import Q
from helpers import data,filter,schema
from ..project import projects_service

FIELDS_TO_EXCLUDE=['id']
MODELS={
    "samples": Sample,
    "experiments":Experiment
}

def get_model(model):
    m = MODELS.get(model)
    if m:
        return m
    raise NotFound(description=f"Model: {model} not found")


def get_items_by_project(project_id, model,args):
    
    m = get_model(model)
    project = projects_service.get_project(project_id)

    if model == 'experiments':
        tsv_fields = ['experiment_id','sample_id']
        id_format = project.experiment['id_format']
    else:
        tsv_fields = ['sample_id']
        id_format = project.sample['id_format']


    
    filter = get_filter(args.get('filter'), model)

    selected_fields = [f"metadata.{v}" for k, v in args.items(multi=True) if k.startswith('fields[]')]

    if not selected_fields:
        
        selected_fields = [f"metadata.{field}" for field in id_format]

    tsv_fields.extend(selected_fields)

    return data.get_items(args, 
                                 m, 
                                 FIELDS_TO_EXCLUDE, 
                                 filter,
                                 tsv_fields,
                                 project_id)

def get_filter(filter, model):
    if not filter:
        return None
    if model == 'samples':
        return (Q(sample_id__iexact=filter) | Q(sample_id__icontains=filter))
    return (Q(experiment_id__iexact=filter) | Q(experiment_id__icontains=filter))

def get_item(project_id, model, item_id):
    db_model = get_model(model)
    query = {"project":project_id}

    if model == 'samples':
        query["sample_id"] = item_id
    else:
        query["experiment_id"] = item_id
    
    item = db_model.objects(**query).first()
    if not item:
        raise NotFound(description=f"{item_id} not found")
    return item
    
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
            "metadata":data
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


def update_item(project_id, model, item_id,data):
    
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
    
    if item_id != new_item_id:
        message = f"{key} {item_id} has changed into {new_item_id}, the value of the fields {','.join(id_fields)} can't be changed"
        raise BadRequest(description=message)
    
    evaluation_errors = filter.evaluate_fields(project, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    
    item.update(metadata=data)
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

def get_model_field_stats(project_id, model, field):

    projects_service.get_project(project_id)
    db_model = get_model(model)

    pipeline = [
        {"$group" : {"_id" : f"${field}", "count" : {"$sum" : 1}}}
    ]
    response = dict()
    for doc in db_model.objects(project=project_id).aggregate(pipeline):
        response[doc["_id"]] = doc["count"]

    #TODO:
    #add datetime parsing
    # print(response)
    
    return data.dump_json(response)
