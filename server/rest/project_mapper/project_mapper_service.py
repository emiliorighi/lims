from db.models import Project
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import  NotFound
from helpers import filter as filter_helper
from helpers.tsv import generate_tsv_reader

def infer_header(project_id, data, files):


    #Validate request payload
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")

    file = files.get('tsv')
    if not file:
        return 'tsv is mandatory', 400
    
    model=data.get('model')
    if not model or not model in ['sample', 'experiment']:
        return 'Model is mandatory, choose between sample or experiment', 400

    header_row = data.get('header_row', 0)
    if not filter_helper.validate_number(header_row):
        return 'header_row must be a valid number', 400
    
    #Prepare data
    fields = project[model]['fields']
    tsvreader = generate_tsv_reader(file)
    header = list(tsvreader)[int(header_row)]
    is_experiment = model == 'experiment'
    mapped_header=[]

    #Map data
    for column in header:
        column_lower = column.lower()
        match = False
        if is_experiment:
            sample_fields = ['sampleid','sampleID','sample']
            if any([ f in column_lower or column_lower == f for f in sample_fields]):
                mapped_header.append({'tsv_column': column, 'field_key': 'sample_id'})
                continue
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
