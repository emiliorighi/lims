from db.models import Project,Sample,Experiment
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import BadRequest, NotFound
from mongoengine.errors import NotUniqueError
from ..sample.samples_service import update_sample
from ..experiment.experiments_service import update_experiment
from helpers import filter
from helpers.tsv import generate_tsv_dict_reader

    
def upload_tsv(project_id, tsv, data):
    project = Project.objects(project_id=project_id).first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")

    if not tsv:
        return 'file is mandatory', 400
    
    model = data.get('model')
    if not model or not model in ['sample', 'experiment']:
        return 'model is mandatory, choose between sample or experiment', 400
   
    model_doc = Experiment if model == 'experiment' else Sample
    map = data.get('map')
    if not map:
        return 'map is mandatory', 400
    
    mapped_values = [m.split(':') for m in map.split(',')]
    if not mapped_values or (not mapped_values[0] and mapped_values[1]):
        return f'map values are not valid: {mapped_values}, 400'

    data_model = project[model]
    data_model_required_fields=[f.get('key') for f in data_model.get('fields') if f.get('required')]
    data_model_id_fields = data_model.get('id_format')
    incoming_model_fields = [t[1] for t in mapped_values]
    
    missing_id_fields=[]
    for id_field in data_model_id_fields:
        if not id_field in incoming_model_fields:
            missing_id_fields.append(id_field)
    
    if missing_id_fields:
        return f"The following fields used to generate the id of {model} are missing {', '.join(missing_id_fields)}", 400
    
    missing_required_fields = []
    for req_field in data_model_required_fields:
        if not req_field in incoming_model_fields:
            missing_required_fields.append(req_field)

    if missing_required_fields:
        return f"The following required fields of {model} are missing {', '.join(missing_required_fields)}", 400
    
    behaviour = data.get('behaviour', 'SKIP')
    valid_map = {t[0]:t[1] for t in mapped_values if t[1]}

    tsvreader = generate_tsv_dict_reader(tsv)
    
    items=[]
    for row in tsvreader:
        item = {}
        for k,v in valid_map.items():
            value = row.get(k)
            if value:
                item[v] = row[k]
        items.append(item)

    header=2
    saved_items = []
    skipped_items = set()
    updated_items = set()
    id_set = set()
    for index, obj in enumerate(items):
        obj_id = create_model_id(data_model_id_fields, obj)
        
        if not obj_id:
            raise BadRequest(description=f"row {header+index}: Unable to generate {model}_id with the fields provided")
        
        if obj_id in id_set:
            continue #SKIP REPEATED OBJECTS
        
        missing_fields = [req_field for req_field in data_model_required_fields 
                  if req_field not in obj or obj[req_field] in [None, '', [], {}]]
    
        if missing_fields:
            raise BadRequest(description=f"row {header+index} {', '.join(missing_fields)} is/are mandatory for {model} ")
        
        evaluation_errors = filter.evaluate_fields(project, obj)
        if evaluation_errors:
            raise BadRequest(description=f"row {header+index} {'; '.join(evaluation_errors)} for {model} ")
        
        doc_to_save={f"{model}_id":obj_id, 'project':project_id, 'metadata':obj }
        if model == 'experiment':
            sample_id = doc_to_save.get('metadata').get('sample_id')
            if not sample_id:
                raise BadRequest(description=f"{sample_id} is missing in {model} at row {header+index}")
            elif not Sample.objects(project=project_id, sample_id=sample_id).first():
                raise BadRequest(description=f"row {header+index}: {sample_id} is not present in the database created it first! ")

            doc_to_save['sample_id'] = sample_id
        try:

            saved_item = model_doc(**doc_to_save).save()
            saved_items.append(saved_item)
            id_set.add(obj_id)

        except NotUniqueError as e:
            if behaviour == 'UPDATE':
                if obj_id in updated_items: continue
                if model == 'sample':
                    message, status = update_sample(project_id, obj_id, doc_to_save['metadata'])
                else:
                    message, status = update_experiment(project_id, obj_id, doc_to_save['metadata'])
                if status == 201:
                    updated_items.add(obj_id)
            else:
                if not obj_id in skipped_items:
                    skipped_items.add(obj_id)
                continue
        except Exception as e:
            raise BadRequest(description=f"row {header+index}: {e}")

    return f'Created: {len(saved_items)}, Skipped:  {len(skipped_items)}, Updated: {len(updated_items)}', 200

def create_model_id(id_fields, data):
    return '_'.join(str(data.get(attr)) for attr in id_fields)
