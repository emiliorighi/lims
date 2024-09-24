from db.models import Project,Sample,Experiment
from werkzeug.exceptions import BadRequest, NotFound
from mongoengine.errors import NotUniqueError
from ..item.items_service import update_item
from helpers import filter
from helpers.tsv import generate_tsv_dict_reader

    
def upload_tsv(project_id, tsv, data):
    """Upload TSV 
        Steps:
        - get project
        - validate tsv
        - get and validate model
        - validate mapper
        - parse mapper
        - validate fields
        - extract items
        - process items
    """

    project = get_project(project_id)

    validate_tsv(tsv)

    model = validate_model(data.get('model'))
   
    model_doc = Experiment if model == 'experiment' else Sample

    mapper = validate_map(data.get('map'))
    
    mapped_values = parse_map(mapper)

    data_model = project[model]

    required_fields = [f.get('key') for f in data_model.get('fields') if f.get('required')]
    id_fields = data_model.get('id_format')

    validate_fields( mapped_values, required_fields, id_fields)

    behaviour = data.get('behaviour', 'SKIP')

    valid_map = {t[0]: t[1] for t in mapped_values if t[1]}
    
    items = extract_items_from_tsv(tsv, valid_map)

    return process_items(items, data_model, model, project, model_doc, behaviour)


def create_model_id(id_fields, data):
    return '_'.join(str(data.get(attr)) for attr in id_fields)


def get_project(project_id):
    """Retrieves the project by ID or raises a NotFound exception."""
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")
    return project


def validate_tsv(tsv):
    """Validates that a TSV file is provided."""
    if not tsv:
        raise BadRequest(description='File is mandatory')


def validate_model(model):
    """Validates that a model is specified and is either 'sample' or 'experiment'."""
    if not model or model not in ['sample', 'experiment']:
        raise BadRequest(description='Model is mandatory, choose between sample or experiment')
    return model

def validate_map(map):
    """Validates that a map is provided."""
    if not map:
        raise BadRequest(description='Map is mandatory')
    return map


def parse_map(map):
    """Parses the mapping string into a list of tuples."""
    mapped_values = [m.split(':') for m in map.split(',')]
    if not mapped_values or (not mapped_values[0] and mapped_values[1]):
        raise BadRequest(description=f'Map values are not valid: {mapped_values}')
    return mapped_values


def validate_fields( mapped_values, required_fields, id_fields):
    """Validates required and ID fields against incoming mapped values."""
    incoming_fields = [t[1] for t in mapped_values]

    missing_id_fields = [field for field in id_fields if field not in incoming_fields]
    if missing_id_fields:
        raise BadRequest(description=f"The following ID fields are missing: {', '.join(missing_id_fields)}")

    missing_required_fields = [field for field in required_fields if field not in incoming_fields]
    if missing_required_fields:
        raise BadRequest(description=f"The following required fields are missing: {', '.join(missing_required_fields)}")

def extract_items_from_tsv(tsv, valid_map):
    """Extracts and maps items from the TSV based on the valid mapping."""
    tsvreader = generate_tsv_dict_reader(tsv)
    items = []
    
    for row in tsvreader:
        item = {valid_map[k]: row[k] for k in valid_map if row.get(k)}
        items.append(item)
    
    return items

def process_items(items, data_model, model, project, model_doc, behaviour):
    """Processes the items, saving them or updating as necessary."""
    saved_items = []
    skipped_items = set()
    updated_items = set()
    id_set = set()
    header = 2  # Starting header line for error reporting

    for index, obj in enumerate(items):
        obj_id = create_model_id(data_model.get('id_format'), obj)
        if not obj_id:
            raise BadRequest(description=f"Row {header + index}: Unable to generate ID")

        if obj_id in id_set:
            continue  # Skip repeated objects

        validate_item(obj, data_model, project, header + index)

        doc_to_save = {f"{model}_id": obj_id, 'project': project.project_id, **obj}
        
        try:
            saved_item = model_doc(**doc_to_save).save()
            saved_items.append(saved_item)
            id_set.add(obj_id)

        except NotUniqueError:
            handle_not_unique_error(obj_id,model, behaviour, doc_to_save, updated_items, skipped_items, header + index)
        except Exception as e:
            raise BadRequest(description=f"Row {header + index}: {e}")

    return f'Created: {len(saved_items)}, Skipped: {len(skipped_items)}, Updated: {len(updated_items)}', 200


def validate_item(obj, data_model, project, row_index):
    """Validates that all required fields are present in the item."""
    required_fields = [f.get('key') for f in data_model.get('fields') if f.get('required')]
    
    missing_fields = [field for field in required_fields if field not in obj or obj[field] in [None, '', [], {}]]
    if missing_fields:
        raise BadRequest(description=f"Row {row_index}: {'; '.join(missing_fields)} is/are mandatory")

    evaluation_errors = filter.evaluate_fields(project, obj)
    if evaluation_errors:
        raise BadRequest(description=f"Row {row_index}: {'; '.join(evaluation_errors)}")


def handle_not_unique_error(obj_id,model, behaviour, doc_to_save, updated_items, skipped_items, project_id):
    """Handles the NotUniqueError by updating or skipping the item based on the behaviour."""
    if behaviour == 'UPDATE':
        if obj_id not in updated_items:
            message, status = update_item(project_id,model, obj_id, doc_to_save)
            if status == 201:
                updated_items.add(obj_id)
    else:
        skipped_items.add(obj_id)