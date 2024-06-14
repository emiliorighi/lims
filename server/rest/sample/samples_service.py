import csv
from io import StringIO
from itertools import islice
from db.models import Sample,Project
# from errors import NotFound
from ..utils import utils
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from mongoengine.queryset.visitor import Q

def get_samples(project_id, offset=0, 
                limit=20, sort_column=None,
                sort_order='asc', **filters):
    project = utils.get_documents_by_query(Project, dict(project_id=project_id))
    if not project.first():
        raise NotFound(f"Project: {project_id} not found!")
    samples = utils.get_documents_by_query(Sample, dict(project=project_id))
    if filters:
        query=dict()
        for key in filters:
            val = filters[key]
            if utils.validate_number(val):
                val = float(val)
            query[f"metadata__{key}"] = val
        samples = samples.filter(**query)
    samples = samples.exclude('id', 'created')
    if sort_column:
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        samples = samples.order_by(sort)
    return samples.count(), samples[int(offset):int(offset)+int(limit)]

def create_filter(key, value):
    contains_k = f"metadata__{key}__icontains"
    exact_k = f"metadata__{key}__iexact"
    return Q(contains_k=value) | Q(exact_k=value)

def get_sample(project_id, sample_id):
    query=dict(project=project_id,sample_id=sample_id)
    sample = Sample.objects(**query).exclude('id','created').first()
    if sample:
        return sample
    raise NotFound(description=f"Sample: {sample_id} not found")

def create_sample_id(id_fields, data):
    return '_'.join(str(data.get(attr)) for attr in id_fields)

def create_sample(project_id, data):
    query=dict(project_id=project_id)
    project = utils.get_documents_by_query(Project,query).first()
    
    if not project:
        raise NotFound(description=f"Project: {project_id} not found")
    
    # Get required fields and id fields from project definition
    id_fields = project.sample.get('id_format', [])

    # Generate sample ID based on id fields
    sample_id = create_sample_id(id_fields, data)
    # Check if sample ID could be generated
    if not sample_id:
        raise BadRequest(description="Unable to generate sample_d with the fields provided")
    
    samples_query = dict(sample_id=sample_id,project=project_id)
    samples = utils.get_documents_by_query(Sample,samples_query)    

    if samples.first():
        raise Conflict(description=f"Sample: {sample_id} already exists!")
    
    # Check for missing required fields
    required_fields = [f['key'] for f in project.sample['fields'] if f.get('required')]
    missing_fields = [req_field for req_field in required_fields if req_field not in data or not data.get(req_field)]
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
    project = utils.get_documents_by_query(Project,query).first()
    if not project:
        raise NotFound(descritpion=f"Project: {project_id} not Found")
    query['sample_id'] = sample_id
    sample = utils.get_documents_by_query(Sample,dict(project=project_id))   
    if not sample.first():
        raise NotFound
    
       # Get required fields and id fields from project definition
    id_fields = project.sample.get('id_format', [])
    # Generate sample ID based on id fields
    new_sample_id = create_sample_id(id_fields, data)
    if sample_id != new_sample_id:
        message = f"Sample ID {sample_id} has changed into {new_sample_id}, the value of the fields {','.join(id_fields)} can't be changed"
        return BadRequest(description=message)
    evaluation_errors = utils.evaluate_fields(project, data)
    if evaluation_errors:
        return BadRequest(description=f"{'; '.join(evaluation_errors)}")
    sample.update(metadata=data)
    return [f"Sample {sample_id} successfully updated"], 201

def delete_sample(project_id, sample_id):
    query=dict(project_id=project_id)
    project = utils.get_documents_by_query(Project,query).first()
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

    project_query=dict(project_id=project_id)
    project = utils.get_documents_by_query(Project, project_query).first()
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

