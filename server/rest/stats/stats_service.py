from db.models import Project,ProjectDraft,Sample,Experiment

MODEL_MAP={
    'projects':Project,
    'project_drafts':ProjectDraft,
    'samples':Sample,
    'experiments':Experiment
}


def lookup_data():
  lookup_response = dict()
  for k,v in MODEL_MAP.items():
      lookup_response[k] = v.objects.count()
  return lookup_response

def get_model_stats(model, field):
  db_model = MODEL_MAP.get(model)
  if not db_model:
      return f"model must be one of {' ,'.join(MODEL_MAP.keys())}",400
  pipeline = [
      {"$group" : {"_id" : f"${field}", "count" : {"$sum" : 1}}}
  ]

  response = dict()
  for doc in db_model.objects.aggregate(pipeline):
      response[doc["_id"]] = doc["count"]
  return response
