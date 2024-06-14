from db.models import Project,ProjectDraft
from mongoengine.queryset.visitor import Q
from jsonschema import validators
import json,yaml,requests
from ..utils import utils
from werkzeug.exceptions import NotFound
import csv
from io import StringIO

JSON_SCHEMA_PATH='/server/project-spec.json'

def get_project(project_id):
    projects = utils.get_documents_by_query(Project, dict(project_id=project_id), ('id','created'))
    if projects.first():
        return projects.as_pymongo()[0]
    raise NotFound(description=f"Project: {project_id} not found!")

def get_projects(offset=0,limit=20,
                filter=None,sort_order=None):
    if filter:
        projects= Project.objects((Q(name__icontains=filter) | Q(name__iexact=filter))).exclude('id','created')
    else:
        projects = Project.objects().exclude('id','created')
    if sort_order:
        sort_column = "name"
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        projects = projects.order_by(sort)
    return projects.count(), projects[int(offset):int(offset)+int(limit)]

def create_project(data):
    errors = []
    errors.extend(jsonschema_validation(data))
    if errors:
        return errors, 401
    for m in ['sample','experiment']:
        model = data.get(m)
        if model:
            errors.extend(validate_model(data.get(m)))
        if errors:
            return errors, 401
        for id_field in model.get('id_format'):
            for attr in model.get('fields'):
                if attr['key'] == id_field:
                    attr['required'] = True

    #change id fields to required
    # print(data)
    project_to_save = Project(**data)
    if utils.get_documents_by_query(Project,dict(project_id=project_to_save.project_id)).first():
        return [f"Project: {project_to_save.project_id} already exists"], 401
    project_draft = utils.get_documents_by_query(ProjectDraft,dict(project_id=project_to_save.project_id))
    if project_draft.first():
        project_draft.delete()
    project_to_save.save()
    return [f"Project {project_to_save.project_id} correctly saved"], 201

def validate_project(data, format='json'):

    content = data
    if format == 'yaml':
        try:
            content = yaml.safe_load(data)
        except yaml.YAMLError as e:
            return {'error': 'Failed to parse YAML', 'details': str(e)}, 400
    errors = jsonschema_validation(content)
    for m in ['sample','experiment']:
        model = content.get(m)
        if model:
            errors.extend(validate_model(model))
    if errors:
        return errors, 400
    else:
        return [f"Project {content.get('project_id')} is valid!"], 200
    

def validate_model(model):
    errors = []
    for id_field in model.get('id_format'):
        if not any(id_field == f['key'] for f in model['fields']):
            errors.append(f"{id_field} not found")
    return errors

def jsonschema_validation(project):
    errors_collection = []
    with open(JSON_SCHEMA_PATH, 'r') as file:
        data = json.load(file)        
        v = validators.Draft202012Validator(data)
        errors = v.iter_errors(project)
        for error in errors:
            errors_collection.append(dict(message=error.message ,path=error.json_path))
    return errors_collection

## guess attribute types from tsv
def map_attributes_from_tsv(tsv, data):
    treshold = int(data.get('treshold', 25))
    tsv_data = StringIO(tsv.read().decode('utf-8'))
    tsvreader = csv.DictReader(tsv_data, delimiter='\t')
    
    mapped_values = {}
    multi_select_candidates = {}
    total_rows = 0

    for row in tsvreader:
        total_rows += 1
        for key, value in row.items():
            if value:
                if key not in mapped_values:
                    mapped_values[key] = set()
                if ',' in value:
                    multi_select_candidates[key] = set()
                    values = [v.strip() for v in value.split(',') if v.strip()]
                    mapped_values[key].update(values)
                    multi_select_candidates[key].update(values)
                else:
                    mapped_values[key].add(value)

    attributes = []
    
    for attr_key, opts in mapped_values.items():
        options = list(opts)
        num_unique_values= len(options)
        filter = {}

        if num_unique_values < total_rows * (treshold / 100):
            filter['choices'] = options
            filter['multi'] = False
        elif num_unique_values <= 10:  # Fewer than or equal to 10 unique values
            filter['choices'] = options
            filter['multi'] = False
        elif attr_key in multi_select_candidates:  # Check if there are any multi-select candidates
            multi_select_options = list(multi_select_candidates[attr_key])
            multi_select_unique_values = len(multi_select_options)
            if multi_select_unique_values <= 10 or multi_select_unique_values < total_rows * (treshold / 100):
                filter['choices'] = multi_select_options
                filter['multi'] = True
        else:
            if all(utils.validate_date(option) for option in options if option):
                filter['input_type'] = 'date'
            elif all(utils.validate_number(option) for option in options if option):
                filter['input_type'] = 'number'
            else:
                filter['input_type'] = 'text'

        attribute = {
            'key': attr_key,
            'label': attr_key,
            'required': False,
            'filter': filter
        }
        attributes.append(attribute)

    return attributes