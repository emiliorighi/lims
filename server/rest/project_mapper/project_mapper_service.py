from db.models import Project
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import  NotFound
from helpers import filter
from helpers.tsv import generate_tsv_dict_reader,generate_tsv_reader

## guess filter types from tsv
def map_attributes_from_tsv(tsv, data):
    treshold = int(data.get('treshold', 25))
    tsvreader = generate_tsv_dict_reader(tsv)
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
    percentage=treshold*total_rows / 100
    print(treshold)
    print(percentage)
    for attr_key, opts in mapped_values.items():
        options = list(opts)
        num_unique_values= len(options)
        filter = {}
        if num_unique_values >= percentage:
            filter['choices'] = options
            filter['multi'] = False
        # elif num_unique_values <= 10:  # Fewer than or equal to 10 unique values
        #     filter['choices'] = options
        #     filter['multi'] = False
        elif attr_key in multi_select_candidates:  # Check if there are any multi-select candidates
            multi_select_options = list(multi_select_candidates[attr_key])
            multi_select_unique_values = len(multi_select_options)
            if  multi_select_unique_values >= percentage:
                filter['choices'] = multi_select_options
                filter['multi'] = True
        else:
            if all(filter.validate_date(option) for option in options if option):
                filter['input_type'] = 'date'
            elif all(filter.validate_number(option) for option in options if option):
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


def infer_fields(project_id, data, files):

    project = Project.objects(project_id=project_id).first()

    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")

    file = files.get('tsv')

    header_row = data.get('header_row', 0)

    model=data.get('model')
    if not file:
        return 'tsv is mandatory', 400
    
    if not model or not model in ['sample', 'experiment']:
        return 'Model is mandatory, choose between sample or experiment', 400

    if not filter.validate_number(header_row):
        return 'header_row must be a valid number', 400
    
    fields = project[model]['fields']

    tsvreader = generate_tsv_reader(file)

    header = list(tsvreader)[int(header_row)]
    mapped_header=[]

    for column in header:
        column_lower = column.lower()
        match = False

        # Iterate over each field to find the best match
        for field in fields:
            if match:
                break
            key = field.get('key', '')
            key_lower = key.lower()

            # Check for exact or partial match
            if column_lower == key_lower or column_lower in key_lower or key_lower in column_lower:
                mapped_header.append({'tsv_column': column, 'field_key': key})
                match = True
        
        # If no match was found, add an entry with an empty field_key
        if not match:
            mapped_header.append({'tsv_column': column, 'field_key': ''})

    return mapped_header, 200
