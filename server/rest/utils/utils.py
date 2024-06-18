from dateutil import parser
import re

def test_regex(pattern, value):
    if re.match(pattern, value):
        return True
    else:
        return False

def validate_date(date_text):
    try:
        parser.parse(date_text)
        return True
    except Exception as e:
        print(e)
        return False
    
def validate_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False   

def evaluate_fields(project, data):
    evaluation_errors = []
    for field in project.sample['fields']:
        filter = field['filter']
        value = data.get(field['key'])
        if value == None:
            continue
        if 'input_type' in filter:
            evaluation_errors.extend(evaluate_input(filter['input_type'], field, value))    
        elif 'choices' in filter:
            evaluation_errors.extend(evaluate_choices( filter['choices'], value))
        elif 'min' in filter and value is not None:
            min_val, max_val = filter.get('min'), filter.get('max')
            evaluation_errors.extend(evaluate_range(min_val,max_val,field,value))
    return evaluation_errors
 
def evaluate_input(input_type, field, value):
    errors = []
    if input_type == 'date' and not validate_date(value):
        errors.append(f"{field['key']} is not a valid date")
    elif input_type == 'number' and not validate_number(value):
        errors.append(f"{field['key']} is not a valid number")
    elif 'regex' in field and not test_regex(field['regex'], value):
        errors.append(f"{value} of {field['key']} does not match {field['regex']}")
    return errors

def evaluate_range(min_val, max_val, field,value):
    errors = []
    if validate_number(value):
        value = float(value)
        if (min_val is not None and value < min_val) or (max_val is not None and value > max_val):
            errors.append(f"{value} must be between {min_val} and {max_val}")
    else:
        errors.append(f"{value} of {field['key']} is not a valid number")
    return errors

def evaluate_choices(choices, value):
    errors= []
    if (isinstance(value, list)):
        for v in value:
            if v.strip() not in choices:
                errors.append(f"{v} is not in {','.join(choices)}")
    else:
        #check for comma separeted values
        value = value.split(',')
        for v in value:
            if v.strip() not in choices:
                errors.append(f"{value} is not in {','.join(choices)}")
    return errors        

def get_documents_by_query(model, query, fields_to_exclude= None):
    if fields_to_exclude:
       query_set =  model.objects(**query).exclude(*fields_to_exclude)
    else:
        query_set = model.objects(**query)
    return query_set
