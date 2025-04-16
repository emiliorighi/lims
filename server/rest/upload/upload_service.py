from db.models import ResearchProject, ResearchModel,ResearchItem
from werkzeug.exceptions import BadRequest, NotFound
from mongoengine.errors import NotUniqueError
from helpers import filter, user as user_helper
from helpers.tsv import generate_tsv_dict_reader
import json
    
def upload_tsv(project_id, tsv, data):
    user = user_helper.get_current_user()
    project = get_project(project_id)
    if not tsv:
        raise BadRequest(description='file field is mandatory')
    model_name = data.get('model')
    
    if not model_name or model_name not in project.models:
        raise BadRequest(description=f"model field is mandatory, choose between {' ,'.join(project.models)}")

    model = ResearchModel.objects(project_id=project_id, name=model_name).first()

    if not model:
        raise NotFound(description=f"{model_name} not found")
    
    serialized_map = data.get('map')
    if not serialized_map:
        raise BadRequest(description=f"map field is mandatory")

    mapper = {k:v for k,v in json.loads(serialized_map).items() if v}

    serialized_reference_fields = data.get('referenceFields')

    if model.reference_model and not serialized_reference_fields:
        raise BadRequest(description=f"referenceFields field is mandatory for this model")
    
    reference_fields = json.loads(serialized_reference_fields)

    behaviour = data.get('behaviour', 'SKIP')
    header = data.get('header')
    if not filter.validate_number(header):
        raise BadRequest(description=f"header must be a valid number")
    header = int(header)

    validate_fields(mapper.keys(), model)

    return process_records(tsv, mapper, model, reference_fields, project_id, behaviour, user.name, header)


def create_model_id(id_fields, data):
    return '_'.join(str(data.get(attr)) for attr in id_fields)


def get_project(project_id):
    """Retrieves the project by ID or raises a NotFound exception."""
    project = ResearchProject.objects(project_id=project_id).first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")
    return project


def process_records(tsv, map, model, reference_columns, project_id, behaviour, username,header=0):
    saved_items = []
    skipped_items = set()
    updated_items = set()
    id_fields = model.id_format
    model_fields = model.fields
    ref_model_name = model.reference_model
    model_name = model.name
    id_set = set()
    tsvreader = generate_tsv_dict_reader(tsv)

    for idx, row in enumerate(tsvreader):
        if idx <= header:
            continue
        current_idx = header+idx
        item = {k: row[v] for k,v in map.items() if row.get(v)}

        reference_id = "_".join([row[ref_col] for ref_col in reference_columns]) if reference_columns else None
        if reference_id and not ResearchItem.objects(project_id=project_id,model_name=ref_model_name, item_id=reference_id).first():
            raise BadRequest(description=f"Row {current_idx}: reference item {reference_id} not found")
        item_id = create_model_id(id_fields, item)
        if not item_id:
            raise BadRequest(description=f"Row {current_idx}: Unable to generate ID")

        if item_id in id_set:
            continue  # Skip repeated objects

        validate_item(item, model_fields, idx)
        doc_to_save={
            "project_id":project_id,
            "model_name":model_name,
            "reference_id":reference_id,
            "created_by":username,
            "item_id":item_id,
            **item
        }
        try:
            item_id = doc_to_save.get('item_id')
            saved_item = ResearchItem(**doc_to_save).save()
            saved_items.append(saved_item)
            id_set.add(item_id)
        except NotUniqueError:
            if behaviour == 'UPDATE':
                if item_id not in updated_items:
                    item_to_update = ResearchItem.objects(project_id=project_id, model_name=model_name, item_id=item_id).first()
                    item_to_update.update(**item)
                    updated_items.add(item_id)
            else:
                skipped_items.add(item_id)        
        except Exception as e:
            raise BadRequest(description=f"Row {current_idx}: {e}")

    return f'Created: {len(saved_items)}, Skipped: {len(skipped_items)}, Updated: {len(updated_items)}'

def validate_item(obj, model_fields, row_index):
    """Validates that all required fields are present in the item."""
    required_fields = [f.get('key') for f in model_fields if f.get('required')]
    missing_fields = [field for field in required_fields if field not in obj or obj[field] in [None, '', [], {}]]
    if missing_fields:
        raise BadRequest(description=f"Row {row_index}: {'; '.join(missing_fields)} is/are mandatory")

    evaluation_errors = filter.evaluate_model_fields(model_fields, obj)
    if evaluation_errors:
        raise BadRequest(description=f"Row {row_index}: {'; '.join(evaluation_errors)}")

def validate_fields( incoming_fields, model):
    """Validates required and ID fields against incoming mapped values."""

    required_fields = [f.get('key') for f in model.fields if f.get('required')]
    id_fields = model.id_format

    missing_id_fields = [field for field in id_fields if field not in incoming_fields]
    if missing_id_fields:
        raise BadRequest(description=f"The following ID fields are missing: {', '.join(missing_id_fields)}")

    missing_required_fields = [field for field in required_fields if field not in incoming_fields]
    if missing_required_fields:
        raise BadRequest(description=f"The following required fields are missing: {', '.join(missing_required_fields)}")
