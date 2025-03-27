import re
from datetime import datetime

def is_valid_date(date: str) -> bool:
    # Regular expression for strict ISO format YYYY-MM-DD
    date_regex = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")

    # Check if the format matches
    if not date_regex.match(date):
        return False

    try:
        # Validate using datetime to catch invalid days (e.g., Feb 30)
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def test_regex(pattern, value):
    regex = re.compile(pattern)
    if validate_number(value):
        return regex.fullmatch(str(value))
    return regex.search( value)

    
def validate_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False   

def evaluate_model_fields(fields, data):
    evaluation_errors = []
    for field in fields:
        filter_type = field.get('type')
        filter_key = field.get('key')
        value = data.get(filter_key)
        if not value:
            continue
        if filter_type == 'select':
            evaluation_errors.extend(evaluate_choices(field.get('choices',[]), value))
        else:
            regex = field.get('regex')
            if(regex and not test_regex(regex, value)):
                evaluation_errors.append(f"{value} of {filter_key} does not match {regex}")
            evaluation_errors.extend(evaluate_input(filter_type, field, value))    
    return evaluation_errors

            
def evaluate_fields(fields, data):
    evaluation_errors = []
    for field in fields:
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
    if input_type == 'date' and not is_valid_date(value):
        errors.append(f"{field['key']} is not a valid date should be of format MM/DD/YYYY and year between 1900 and 2099")
    elif input_type == 'number' and not validate_number(value):
        errors.append(f"{field['key']} is not a valid number")
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

def count_occurences(tsvreader):
    #count how many times a value is encountered
    mapped_values = {}
    counter = 0
    for row in tsvreader:
        counter+=1
        for key, value in row.items():

            #skip empty values
            if not value:
                continue

            if key not in mapped_values:
                mapped_values[key] = dict()

            if ',' in value:
                values = [v.strip() for v in value.split(',') if v.strip()]

                for v in values:
                    if v in mapped_values[key]:
                        mapped_values[key][v] += 1
                    else:
                        mapped_values[key][v] = 1

            if value in mapped_values[key]:
                mapped_values[key][value] += 1
            else:
                mapped_values[key][value] = 1

    return mapped_values, counter