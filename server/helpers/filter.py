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