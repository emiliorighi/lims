from db.models import ResearchItem,ResearchModel,ResearchProject,FileLink
from helpers import data as data_helper
from werkzeug.exceptions import BadRequest,NotFound
from mongoengine.queryset.visitor import Q

"""
fetch records, models, protocols and projects counts
"""
MODELS_MAP = {
    'projects':ResearchProject,
    'models':ResearchModel,
    'records':ResearchItem,
    'links':FileLink,
}

def lookup_data():
  lookup_response = dict()
  for k, v in MODELS_MAP.items():
#   for k,v in MODEL_MAP.items():
      lookup_response[k] = v.objects.count()
  return lookup_response

NO_VALUE_KEY='No Entry'

def get_link_stats(field, imm_dict):
    query = {**imm_dict}
    q_query = None

    parsed_query, q_query = data_helper.create_query(query, q_query)
    items = FileLink.objects(**parsed_query)
    if q_query:
        items = items.filter(q_query)
    return launch_pipeline(field, items)

def get_records_stats(field, imm_dict):
    query = {**imm_dict}
    q_query = None
    parsed_query, q_query = data_helper.create_query(query, q_query)
    items = ResearchItem.objects(**parsed_query)
    if q_query:
        items = items.filter(q_query)
    return launch_pipeline(field, items)

def get_stats(project_id, model_name, field, immutable_dict):
    # Check if the model exists in MODEL_LIST
    query = {**immutable_dict}
    project = ResearchProject.objects(project_id=project_id).first()
    if not project:
        raise NotFound(description=f"Project {project_id} not found")

    model = ResearchModel.objects(name=model_name).first()
    if not model:
        raise NotFound(description=f"Model {model_name} of {project_id} not found")
    filter = query.pop('filter',None)
    
    q_query =(Q(item_id__icontains=filter) | Q(item_id__iexact=filter)) if filter else None

    query = {'project_id':project_id, 'model_name':model_name, **query}  

    parsed_query, q_query = data_helper.create_query(query, q_query)
    items = ResearchItem.objects(**parsed_query)
    if q_query:
        items = items.filter(q_query)

    return launch_pipeline(field, items)

def launch_pipeline(field, items):
    try:
        pipeline = [
            {
                "$project": {
                    "field_value": {
                        "$ifNull": [f"${field}", f"{NO_VALUE_KEY}"]
                    }
                }
            },
            {"$unwind": "$field_value"},
            {
                "$group": {
                    "_id": "$field_value",
                    "count": {"$sum": 1}
                }
            },
        ]

        response = {
            str(doc["_id"]): int(doc["count"])
            for doc in items.aggregate(pipeline)
        }

        sorted_response = {key: value for key, value in sorted(response.items())}
        return data_helper.dump_json(sorted_response)

    except Exception as e:
        print(e)
        raise BadRequest(description=f"{str(e)}")
    
