import csv
from io import StringIO
from itertools import islice
from db.models import Experiment,Project,Sample
from ..utils import utils
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from mongoengine.queryset.visitor import Q
from ..helpers import data

FIELDS_TO_EXCLUDE=['id']

def get_experiments(project_id, args):
    
    project = Project.objects(project_id=project_id).first()
    
    if not project:
        raise NotFound(f"Project: {project_id} not found!")
    
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
    sample = Experiment.objects(project=project_id,experiment_id=experiment_id).exclude('id','created').first()
    if sample:
        return sample
    raise NotFound(description=f"Experiment: {experiment_id} not found")

def create_experiment_id(id_fields, data):
    return '_'.join(str(data.get(attr)) for attr in id_fields)


def create_experiment(project_id, data):

    project = Project.objects(project_id=project_id).first()    
    if not project:
        raise NotFound(description=f"Project: {project_id} not found")
    
    # Get required fields and id fields from project definition
    id_fields = project.experiment.get('id_format', [])

    # Generate sample ID based on id fields
    experiment_id = create_experiment_id(id_fields, data)

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

    # Check for missing required fields
    required_fields = [f['key'] for f in project.experiment['fields'] if f.get('required')]
    missing_fields = [req_field for req_field in required_fields 
                  if req_field not in data or data[req_field] in [None, '', [], {}]]
    
    if missing_fields:
        raise BadRequest(description=f"{', '.join(missing_fields)} is/are mandatory")
    
    evaluation_errors = utils.evaluate_fields(project, data)
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
    project = Project.objects(project_id=project_id).first()
    
    if not project:
        raise NotFound(descritpion=f"Project: {project_id} not Found")
    
    
    experiment = Experiment.objects(project=project_id, experiment_id=experiment_id).first()
    if not experiment:
        raise NotFound(descritpion=f"Experiment: {experiment_id} not Found")
    
       # Get required fields and id fields from project definition
    id_fields = project.experiment.get('id_format', [])
    # Generate sample ID based on id fields
    new_experiment_id = create_experiment_id(id_fields, data)
    if experiment_id != new_experiment_id:
        message = f"Experiment ID {experiment_id} has changed into {new_experiment_id}, the value of the fields {','.join(id_fields)} can't be changed"
        raise BadRequest(description=message)
    evaluation_errors = utils.evaluate_fields(project, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    
    experiment.update(metadata=data)
    return [f"Experiment {experiment_id} successfully updated"], 201

def delete_experiment(project_id, experiment_id):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not Found")
    
    exp_to_delete = Experiment.objects(project=project_id,experiment_id=experiment_id).first()
    if not exp_to_delete:
        raise NotFound(description=f"Experiment: {experiment_id} not found")
    
    exp_to_delete.delete()
    return f"Experiment {experiment_id} successfully deleted", 201

def upload_experiments(project_id, files_dict, payload):

    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound(f"Project: {project_id} not found!")
    
    report = files_dict.get('experiment_tsv')
    if not report:
        raise BadRequest(description=f"experiment_tsv field must contain a tsv file")
    
    for field in project.experiment['fields']:
        if not field['required']:
            continue
        if not payload.get(field['key']):
            raise BadRequest(description=f"{field['key']} is a required field to map")
    
    sample_id_field = payload.get('sample_id')
    if not sample_id_field:
        raise BadRequest(description=f"sample_id is a required field to map")

    experiments = StringIO(report.read().decode('utf-8'))
    experiments = islice(experiments, None, None)
    tsvreader = csv.DictReader(experiments, delimiter='\t')

    mapped_experiments = []
    for index, row in enumerate(tsvreader):
        mapped_exp = dict()
        for k in payload:
            mapped_exp[k] = row[payload[k]]
        mapped_experiments.append(mapped_exp)

    evaluation_errors=[]   
    for index, mapped_exp in enumerate(mapped_experiments):
        errors = utils.evaluate_fields(project, mapped_exp)
        if errors:
            evaluation_errors.append(dict(row=index, messages=errors))
    if evaluation_errors:
        return evaluation_errors, 400 #custom bad request
    
    exp_to_save = [Experiment(**mapped_exp) for mapped_exp in mapped_experiments]

    sample_id_list = [exp.sample_id for exp in exp_to_save]
    existing_samples = Sample.objects(project=project_id, sample_id__in=sample_id_list).scalar('sample_id')
    missing_samples = [missing_id for missing_id in sample_id_list if not missing_id in existing_samples ]
    if missing_samples:
        raise BadRequest(description=f"The following samples are missing {' ,'.join(missing_samples)}")
    
    Experiment.insert(exp_to_save)
    #VALIDATE SAMPLES
    return f"A total of {len(exp_to_save)} samples successfully saved",201

