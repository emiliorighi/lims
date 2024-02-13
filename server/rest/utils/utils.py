from errors import NotFound
from db.models import Project
from dateutil import parser
from dateutil.parser import ParserError
import re

def test_regex(pattern, value):
    if re.match(pattern, value):
        return True
    else:
        return False

def validate_date(date_text):
    try:
        date_obj = parser.parse(date_text)
        return True
    except ParserError:
        return False
    
def validate_number(number):
    try:
        float(number)  # or int(s) if you only want to consider integers
        return True
    except ValueError:
        return False   

def evaluate_fields(project, data):
    evaluation_errors = []
    
    for field in project.sample['fields']:
        value = data.get(field['key'])
        
        if 'input_type' in field:
            input_type = field['input_type']
            if input_type == 'date' and not validate_date(value):
                evaluation_errors.append(f"{field['key']} is not a valid date")
            elif input_type == 'number' and not validate_number(value):
                evaluation_errors.append(f"{field['key']} is not a valid number")
            elif 'regex' in field and not test_regex(field['regex'], value):
                evaluation_errors.append(f"{value} of {field['key']} does not match {field['regex']}")
                
        elif 'choices' in field:
            choices = field['choices']
            if (isinstance(value, list) and any(v not in choices for v in value)) or (value not in choices):
                evaluation_errors.append(f"{value} is not in {','.join(choices)}")
        
        elif 'min' in field and value is not None:
            min_val, max_val = field.get('min'), field.get('max')
            if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
                evaluation_errors.append(f"{value} must be between {min_val} and {max_val}")
    
    return evaluation_errors
 
def return_document_by_id(model, query, fields_to_exclude= None):
    if fields_to_exclude:
       query_set =  model.objects(**query).exclude(*fields_to_exclude)
    else:
        query = model.objects(**query)
    if not query_set.first():
        raise NotFound
    return query_set.as_pymongo()[0]


def delete_document(model, query):
    document = model.objects(**query).first()
    if not document:
        raise NotFound
    
def get_document(model, query, fields_to_exclude=None):
    query_set = model.objects(**query)
    if not query_set.first():
        raise NotFound
    if fields_to_exclude:
        query_set = query_set.exclude(*fields_to_exclude)
    return query_set.as_pymongo()[0]

# def validate_model_id(project_id, data, model):
#     project = Project.objects(project_id=project_id).first()
#     if not project:
#         raise NotFound
#     # Fetch samples for the project
#     samples = model.objects(project=project.project_id)
#     # Get required fields and id fields from project definition
#     id_fields = project.sample.get('id_fields', [])
#     # Generate sample ID based on id fields
#     sample_id = '_'.join(str(data.get(attr)) for attr in id_fields)
#     # Check if sample ID could be generated
#     if not sample_id:
#         return ["Unable to generate ID with specified fields"], 400
#     # Check if the sample already exists
#     if samples.filter(sample_id=sample_id).first():
#         return [f"Sample {sample_id} already exists!"], 400
#     return 

# def validate_fields_against_project(dict_fields, project_model):
#     errors = []
#     project_model
