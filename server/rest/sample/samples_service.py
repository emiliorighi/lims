from db.models import Sample,Project
from errors import NotFound
from ..utils import utils

def get_samples(project_id, offset=0, 
                limit=20, sort_column=None,
                sort_order='asc', **filters):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound
    samples = Sample.objects(project=project_id)
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

def get_sample(project_id, sample_id):
    samples = Sample.objects(project=project_id,sample_id=sample_id).exclude('id','created')
    if not samples.first():
        raise NotFound
    return samples.as_pymongo()[0]

def create_sample(project_id, data):
    project = Project.objects(project_id=project_id).first()
    
    if not project:
        raise NotFound
    
    # Fetch samples for the project
    samples = Sample.objects(project=project.project_id)
    
    # Get required fields and id fields from project definition
    id_fields = project.sample.get('id_format', [])

    # Generate sample ID based on id fields
    sample_id = '_'.join(str(data.get(attr)) for attr in id_fields)
    
    # Check if sample ID could be generated
    if not sample_id:
        return ["Unable to generate ID with specified fields"], 400
    
    # Check if the sample already exists
    if samples.filter(sample_id=sample_id).first():
        return [f"Sample {sample_id} already exists!"], 400

    # Check for missing required fields
    required_fields = [f['key'] for f in project.sample['fields'] if f.get('required')]
    missing_fields = [req_field for req_field in required_fields if req_field not in data or not data.get(req_field)]
    if missing_fields:
        return [f"{', '.join(missing_fields)} is/are mandatory"], 400
    
    evaluation_errors = utils.evaluate_fields(project, data)
    if evaluation_errors:
        return evaluation_errors, 400
    print(data)
    new_sample = Sample(
        project=project_id,
        sample_id=sample_id,
        metadata=data
    ).save()

    return [f"Sample {sample_id} of {project_id} correctly saved!"], 201  # Return the created sample with 201 Created status


def update_sample(project_id,sample_id,data):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound
    sample = Sample.objects(project=project_id,sample_id=sample_id)
    if not sample.first():
        raise NotFound
       # Get required fields and id fields from project definition
    id_fields = project.sample.get('id_format', [])

    # Generate sample ID based on id fields
    new_sample_id = '_'.join(str(data.get(attr)) for attr in id_fields)
    if sample_id != new_sample_id:
        message = f"Sample ID {sample_id} has changed into {new_sample_id}, the value of the fields {','.join(id_fields)} can't be changed"
        return [message], 400
    evaluation_errors = utils.evaluate_fields(project, data)
    if evaluation_errors:
        return evaluation_errors, 400
    sample.update(metadata=data)
    return [f"Sample {sample_id} successfully updated"], 201

def delete_sample(project_id, sample_id):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound
    sample = Sample.objects(project=project_id,sample_id=sample_id)
    if not sample.first():
        raise NotFound
    sample.delete()
    return[ f"Sample {id} successfully deleted"],201
