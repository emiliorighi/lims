from db.models import Sample,Project
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from mongoengine.queryset.visitor import Q
from helpers import data,filter,schema
from ..project import projects_service

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

def create_sample(project_id, data):

    project = projects_service.get_project(project_id)
    
    id_fields = project.sample.get('id_format', [])

    sample_id = schema.create_item_id(id_fields, data)

    # Check if sample ID could be generated
    if not sample_id:
        raise BadRequest(description="Unable to generate sample_id with the fields provided")
    
    sample = Sample.objects(project=project_id, sample_id=sample_id).first()   

    if sample:
        raise Conflict(description=f"Sample: {sample_id} already exists!")
    
    missing_fields = schema.validate_required_fields(project.sample,data)
    if missing_fields:
        raise BadRequest(description=f"{', '.join(missing_fields)} is/are mandatory")
    
    evaluation_errors = filter.evaluate_fields(project, data)
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

    project=projects_service.get_project(project_id)
        
    id_fields = project.sample.get('id_format', [])

    new_sample_id = schema.create_item_id(id_fields, data)

    if new_sample_id and sample_id != new_sample_id:
        message = f"Sample ID {sample_id} has changed into {new_sample_id}, the value of the fields {','.join(id_fields)} can't be changed"
        raise BadRequest(description=message)
    
    evaluation_errors = filter.evaluate_fields(project, data)
    if evaluation_errors:
        raise BadRequest(description=f"{'; '.join(evaluation_errors)}")
    
    sample.update(metadata=data)

    return [f"Sample {sample_id} successfully updated"], 201

def delete_sample(project_id, sample_id):

    projects_service.get_project(project_id)
    
    sample = Sample.objects(project=project_id, sample_id=sample_id).first()   
    
    sample.delete()

    print(sample)
    return f"Sample {sample_id} successfully deleted", 201

