from db.models import Sample,Project,Experiment
from errors import NotFound
from datetime import datetime
from mongoengine.queryset.visitor import Q
from ..utils import utils

def get_experiments(project_id, sample_id=None, offset=0,limit=20,
                    filter=None,filter_field=None,
                    start_date=None, end_date=datetime.utcnow,
                    sort_column=None, sort_order=None):
    query=dict()
    if not Project.objects(project_id=project_id).first():
        raise NotFound
    query['project'] = project_id

    if sample_id:
        if not Sample.objects(project=project_id, sample_id=sample_id).first():
            raise NotFound
        query['sample_id'] = sample_id
    experiments = Experiment.objects(**query)
    filter_query = None
    if filter_field and filter:
        key = f"{filter_query}__icontains"
        query = dict()
        query[key]=filter
        filter_query = (Q(query))
    date_query = None
    if start_date:
        date_query = (Q(created__gte=start_date) & Q(created__lte=end_date))
    if filter_query and date_query:
        experiments = experiments.filter(filter_query & date_query)
    elif filter_query:
        experiments = experiments.filter(filter_query)
    elif date_query:
        experiments = experiments.filter(date_query)
    experiments = experiments.exclude('id', 'created')
    if sort_column:
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        experiments = experiments.order_by(sort)
    return experiments.count(), experiments[int(offset):int(offset)+int(limit)]

def get_experiment(project_id, experiment_id):
    experiments = Sample.objects(project=project_id,experiment_id=experiment_id).exclude('id','created')
    if not experiments.first():
        raise NotFound
    return experiments.as_pymongo()[0]

def create_experiment(project_id, sample_id, data):
    project = Project.objects(project_id=project_id).first()
    
    if not project:
        raise NotFound
    
    # Fetch experiments for the project
    experiments = Experiment.objects(project=project.project_id)
    
    # Get required fields and id fields from project definition
    id_fields = project.experiment.get('id_fields', [])

    # Generate sample ID based on id fields
    experiment_id = '_'.join(str(data.get(attr)) for attr in id_fields)
    
    # Check if sample ID could be generated
    if not experiment_id:
        return ["Unable to generate ID with specified fields"], 400
    
    # Check if the sample already exists
    if experiments.filter(experiment_id_id=experiment_id).first():
        return [f"Sample {experiment_id} already exists!"], 400

    # Check for missing required fields
    required_fields = [f['key'] for f in project.sample['fields'] if f.get('required')]
    missing_fields = [req_field for req_field in required_fields if req_field not in data or not data.get(req_field)]
    if missing_fields:
        return [f"{', '.join(missing_fields)} is/are mandatory"], 400
    
    evaluation_errors = utils.evaluate_fields(project, data)
    if evaluation_errors:
        return evaluation_errors, 400

    new_experiment = Experiment(
        project=project_id,
        sample_id=sample_id,
        experiment_id=experiment_id,
        metadata=data
    ).save()

    return [f"Experiment {experiment_id} of {project_id} correctly saved!"], 201  # Return the created sample with 201 Created status


def update_experiment(project_id,experiment_id,data):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound
    experiment = Experiment.objects(project_id=project_id,experiment_id=experiment_id)
    if not experiment.first():
        raise NotFound
       # Get required fields and id fields from project definition
    id_fields = project.sample.get('id_fields', [])
    # Generate sample ID based on id fields
    new_experiment_id = '_'.join(str(data.get(attr)) for attr in id_fields)
    if experiment_id != new_experiment_id:
        message = f"Experiment {experiment_id} has changed into {new_experiment_id}, the value of the fields {','.join(id_fields)} can't be changed"
        return [message], 400
    evaluation_errors = utils.evaluate_fields(project, experiment.metadata)
    if evaluation_errors:
        return evaluation_errors, 400
    experiment.update(metadata=data)
    return [f"Experiment {experiment_id} successfully updated"], 201

def delete_experiment(project_id, experiment_id):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound
    experiment = Experiment.objects(project_id=project_id,experiment_id=experiment_id)
    if not experiment.first():
        raise NotFound
    experiment.delete()
    return[ f"Sample {id} successfully deleted"],201
