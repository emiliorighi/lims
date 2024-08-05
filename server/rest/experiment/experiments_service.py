from db.models import Experiment,Project,Sample
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from mongoengine.queryset.visitor import Q
from helpers import data,filter,schema
from ..project import projects_service

FIELDS_TO_EXCLUDE=['id']

def get_experiments(args):
    
    filter = get_filter(args.get('filter'))

    tsv_fields = ['experiment_id','sample_id', 'project']

    selected_fields = [f"metadata.{v}" for k, v in args.items(multi=True) if k.startswith('fields[]')]

    if selected_fields:
        
        tsv_fields.extend(selected_fields)

    return data.get_items(args, 
                                 Experiment, 
                                 FIELDS_TO_EXCLUDE, 
                                 filter,
                                 tsv_fields,
                                 None)


def get_experiments_by_project(project_id, args):
    
    project = projects_service.get_project(project_id)
    
    filter = get_filter(args.get('filter'))

    tsv_fields = ['experiment_id','sample_id']

    selected_fields = [f"metadata.{v}" for k, v in args.items(multi=True) if k.startswith('fields[]')]

    if not selected_fields:
        
        selected_fields = [f"metadata.{field}" for field in project.sample['id_format']]

    tsv_fields.extend(selected_fields)

    return data.get_items(args, 
                                 Experiment, 
                                 FIELDS_TO_EXCLUDE, 
                                 filter,
                                 tsv_fields,
                                 project_id)

def get_filter(filter):
    if filter:
        return (Q(experiment_id__iexact=filter) | Q(experiment_id__icontains=filter))
    return None

def get_experiment(project_id, experiment_id):
    experiment = Experiment.objects(project=project_id,experiment_id=experiment_id).exclude('id','created').first()
    if experiment:
        return experiment
    raise NotFound(description=f"Experiment: {experiment_id} not found")

def create_experiment(project_id, data):

    project = projects_service.get_project(project_id)
    
    # Get required fields and id fields from project definition
    id_fields = project.experiment.get('id_format', [])

    # Generate sample ID based on id fields
    experiment_id = schema.create_item_id(id_fields, data)

    # Check if sample ID could be generated
    if not experiment_id:
        raise BadRequest(description="Unable to generate experiment_id with the fields provided")
    
    experiment = Experiment.objects(project=project_id, experiment_id=experiment_id).first()   

    if experiment:
        raise Conflict(description=f"Experiment: {experiment_id} already exists!")
    
    sample_id = data.get('sample_id')
    if not sample_id:
        raise BadRequest(description="sample_id field is mandatory")

    sample_object = Sample.objects(project=project_id, sample_id=sample_id).first()
    if not sample_object:
        raise BadRequest(description=f"Sample {sample_id} does not exist, create it first")

    missing_fields = schema.validate_required_fields(project.experiment, data)
    
    if missing_fields:
        raise BadRequest(description=f"{', '.join(missing_fields)} is/are mandatory")
    
    evaluation_errors = filter.evaluate_fields(project, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    
    try: 
        Experiment(
            project=project_id,
            experiment_id=experiment_id,
            sample_id=sample_id,
            metadata=data
        ).save()

    except Exception as e:
        raise BadRequest(description=e)
    
    return f"Experiment {experiment_id} of {project_id} correctly saved!", 201  # Return the created sample with 201 Created status

def update_experiment(project_id,experiment_id,data):
    
    project =projects_service.get_project(project_id)
    
    experiment = get_experiment(project_id, experiment_id)
    
    id_fields = project.experiment.get('id_format', [])
    new_experiment_id = schema.create_item_id(id_fields, data)
    
    if experiment_id != new_experiment_id:
        message = f"Experiment ID {experiment_id} has changed into {new_experiment_id}, the value of the fields {','.join(id_fields)} can't be changed"
        raise BadRequest(description=message)
    
    evaluation_errors = filter.evaluate_fields(project, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    
    experiment.update(metadata=data)
    return [f"Experiment {experiment_id} successfully updated"], 201

def delete_experiment(project_id, experiment_id):
    
    projects_service.get_project(project_id)
    
    exp_to_delete = get_experiment(project_id,experiment_id)
    
    exp_to_delete.delete()
    return f"Experiment {experiment_id} successfully deleted", 201
