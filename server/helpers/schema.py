from jsonschema import validators
import json,yaml


JSON_SCHEMA_PATH='/server/project-spec.json'

MODELS=['sample','experiment']

def validate_yaml(data):
    try:
        return yaml.safe_load(data),None
    except yaml.YAMLError as e:
        return None, {'error': 'Failed to parse YAML', 'details': str(e)}

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

def validate_content(content):
    """
    Validates the provided content for both jsonschema and model-specific validations.
    """
    errors = jsonschema_validation(content)
    for m in MODELS:
        model = content.get(m)
        if model:
            errors.extend(validate_model(model))
    return errors    


def create_item_id(id_fields,data):
    l = [str(data.get(attr)) for attr in id_fields if data.get(attr)]
    if l:
        return '_'.join(l)
    
def validate_required_fields(model, data):
    
    required_fields = [f['key'] for f in model.get('fields') if f.get('required')]

    missing_fields = [req_field for req_field in required_fields 
                  if req_field not in data or data[req_field] in [None, '', [], {}]]
    
    return missing_fields  