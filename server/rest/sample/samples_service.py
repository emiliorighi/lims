import csv
from io import StringIO
from itertools import islice
from db.models import Sample,Project
from ..utils import utils
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from mongoengine.queryset.visitor import Q
from ..helpers import data

FIELDS_TO_EXCLUDE=['id']

def get_samples(args):
    
    filter = get_filter(args.get('filter'))

    tsv_fields = ['sample_id','project']

    selected_fields = [f"metadata.{v}" for k, v in args.items(multi=True) if k.startswith('fields[]')]

    if selected_fields:
        
        tsv_fields.extend(selected_fields)

    return data.get_items(args, 
                                 Sample, 
                                 FIELDS_TO_EXCLUDE, 
                                 filter,
                                 tsv_fields,
                                 None)


def get_samples_by_project(project_id, args):
    
    project = Project.objects(project_id=project_id).first()
    
    if not project:
        raise NotFound(f"Project: {project_id} not found!")
    
    filter = get_filter(args.get('filter'))

    tsv_fields = ['sample_id']

    selected_fields = [f"metadata.{v}" for k, v in args.items(multi=True) if k.startswith('fields[]')]

    if not selected_fields:
        
        selected_fields = [f"metadata.{field}" for field in project.sample['id_format']]

    tsv_fields.extend(selected_fields)

    return data.get_items(args, 
                                 Sample, 
                                 FIELDS_TO_EXCLUDE, 
                                 filter,
                                 tsv_fields,
                                 project_id)



def get_filter(filter):
    if filter:
        return (Q(sample_id__iexact=filter) | Q(sample_id__icontains=filter))
    return None

def get_sample(project_id, sample_id):
    sample = Sample.objects(project=project_id,sample_id=sample_id).exclude('id','created').first()
    if sample:
        return sample
    raise NotFound(description=f"Sample: {sample_id} not found")

def create_sample_id(id_fields, data):
    l = [str(data.get(attr)) for attr in id_fields if data.get(attr)]
    if l:
        return '_'.join(l)

def create_sample(project_id, data):

    project = Project.objects(project_id=project_id).first()    
    if not project:
        raise NotFound(description=f"Project: {project_id} not found")
    
    # Get required fields and id fields from project definition
    id_fields = project.sample.get('id_format', [])

    # Generate sample ID based on id fields
    sample_id = create_sample_id(id_fields, data)

    # Check if sample ID could be generated
    if not sample_id:
        raise BadRequest(description="Unable to generate sample_id with the fields provided")
    
    sample = Sample.objects(project=project_id, sample_id=sample_id).first()   

    if sample:
        raise Conflict(description=f"Sample: {sample_id} already exists!")
    
    # Check for missing required fields
    required_fields = [f['key'] for f in project.sample['fields'] if f.get('required')]
    missing_fields = [req_field for req_field in required_fields 
                  if req_field not in data or data[req_field] in [None, '', [], {}]]
    
    if missing_fields:
        raise BadRequest(description=f"{', '.join(missing_fields)} is/are mandatory")
    
    evaluation_errors = utils.evaluate_fields(project, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    
    try: 
        Sample(
            project=project_id,
            sample_id=sample_id,
            metadata=data
        ).save()

    except Exception as e:
        raise BadRequest(description=e)


    return f"Sample {sample_id} of {project_id} correctly saved!", 201  # Return the created sample with 201 Created status


def update_sample(project_id,sample_id,data):
    query=dict(project_id=project_id)
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound(descritpion=f"Project: {project_id} not Found")
    query['sample_id'] = sample_id
    sample = Sample.objects(project=project_id, sample_id=sample_id)   
    if not sample.first():
        raise NotFound
    
       # Get required fields and id fields from project definition
    id_fields = project.sample.get('id_format', [])
    # Generate sample ID based on id fields
    new_sample_id = create_sample_id(id_fields, data)
    print(type(new_sample_id))
    if new_sample_id and sample_id != new_sample_id:
        message = f"Sample ID {sample_id} has changed into {new_sample_id}, the value of the fields {','.join(id_fields)} can't be changed"
        raise BadRequest(description=message)
    evaluation_errors = utils.evaluate_fields(project, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    sample.update(metadata=data)
    return [f"Sample {sample_id} successfully updated"], 201

def delete_sample(project_id, sample_id):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not Found")
    sample_to_delete = Sample.objects(project=project_id,sample_id=sample_id).first()
    if not sample_to_delete:
        raise NotFound(description=f"Sample: {sample_id} not found")
    sample_to_delete.delete()
    return f"Sample {sample_id} successfully deleted", 201

# def download_samples(samples):

"""
STEPS:
tsv exists
required fields exists
import project
retrieve sample metadata
test sample value against project field
"""

def upload_samples(project_id, files_dict, payload):

    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound(f"Project: {project_id} not found!")
    
    report = files_dict.get('sample_tsv')
    if not report:
        raise BadRequest(description=f"sample_tsv field must contain a tsv file")
    
    for field in project.sample['fields']:
        if not field['required']:
            continue
        if not payload.get(field['key']):
            raise BadRequest(description=f"{field['key']} is a required field to map")
    
    samples = StringIO(report.read().decode('utf-8'))
    samples = islice(samples, None, None)
    tsvreader = csv.DictReader(samples, delimiter='\t')

    mapped_samples = []
    for index, row in enumerate(tsvreader):
        mapped_sample = dict()
        for k in payload:
            mapped_sample[k] = row[payload[k]]
        mapped_samples.append(mapped_sample)

    evaluation_errors=[]   
    for index, mapped_sample in enumerate(mapped_samples):
        errors = utils.evaluate_fields(project, mapped_sample)
        if errors:
            evaluation_errors.append(dict(row=index, messages=errors))
    if evaluation_errors:
        return evaluation_errors, 400 #custom bad request
    samples_to_save = [Sample(**mapped_sample) for mapped_sample in mapped_samples]

    Sample.insert(samples_to_save)

    #VALIDATE SAMPLES
    return f"A total of {len(samples_to_save)} samples successfully saved",201

