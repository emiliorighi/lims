from db.models import ProjectDraft,Project
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import NotFound
from helpers import schema,tsv as tsv_helper, filter as filter_helper

def get_draft_project(project_id):
    draft_projects=ProjectDraft.objects(project_id=project_id).exclude('id','created').first()
    if draft_projects:
        return draft_projects
    raise NotFound(description=f"Draft Project: {project_id} not found!")

def create_draft_project(data):
    for req_field in ['project_id', 'name','version']:
        if not data.get(req_field):
            message = f"{req_field} is mandatory in ProjectDraft objects"
            status = 400
    if Project.objects(project_id=data['project_id']).first():
        message= f"An existing project with id: {data['project_id']} already exists"
        status = 409
    elif ProjectDraft.objects(project_id=data['project_id']).first():
        message = f"An existing draft project with id: {data['project_id']} already exists"
        status = 409
    else:
        new_draft_project = ProjectDraft(**data)
        new_draft_project.save()
        message = f"Draft project with id: {new_draft_project.project_id} correctly created"
        status = 201
    return [message],status

def update_draft_project(project_id, data):
    projects_to_update = ProjectDraft.objects(project_id=project_id)
    if not projects_to_update.first():
        raise NotFound(description=f"Draft Projects: {project_id} not found!")
    
    projects_to_update.update_one(**data)
    message = f"Draft project {project_id} correctly updated"
    return [message], 201


def get_draft_projects(offset=0,limit=20,
                filter=None,sort_order=None):
    if filter:
        projects= ProjectDraft.objects((Q(name__icontains=filter) | Q(name__iexact=filter))).exclude('id','created')
    else:
        projects = ProjectDraft.objects().exclude('id','created')
    if sort_order:
        sort_column = "name"
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        projects = projects.order_by(sort)
    return projects.count(), projects[int(offset):int(offset)+int(limit)]


def delete_draft_project(project_id):
    project_to_delete=ProjectDraft.objects(project_id=project_id).first()
    if not project_to_delete:
        raise NotFound(description=f"Draft Projects: {project_id} not found!")
    project_to_delete.delete()
    message= f"Draft Project with id: {project_id} successfully deleted"
    return [message], 201


def validate_project(data, format='json'):

    content = data
    if format == 'yaml':
        content, error = schema.validate_yaml(data)
        if error:
            return error, 400
    errors = schema.validate_content(content)

    if errors:
        return errors, 400
    else:
        return [f"Project {content.get('project_id')} is valid!"], 200

def map_attributes_from_tsv(tsv, data):

    validations = {
        'date': filter_helper.validate_date,
        'number': filter_helper.validate_number
    }
    # min_occurrences = int(data.get('min_occurrences', 100))

    tsvreader = tsv_helper.generate_tsv_dict_reader(tsv)

    mapped_values, counter  = filter_helper.count_occurences(tsvreader)

    attributes = []
    for attr_key, values_occurrences in mapped_values.items():

        filter={}
        sum = 0
        for key, count in values_occurrences.items():
            sum+=count
        occ = int(round((sum/counter)*100))

        if occ <= 85:
            filter['choices'] = list(values_occurrences.keys())
            filter['multi'] = False

        else:
            for input_type, validator in validations.items():
                if all(validator(option) for option in values_occurrences.keys()):
                    filter['input_type'] = input_type
                    break
            else:
                filter['input_type'] = 'text'


        attributes.append(
            {
                'key': attr_key,
                'label': attr_key,
                'required': False,
                'filter': filter
            }
        )

    return attributes
