from db.models import Project,ProjectDraft,Sample,Experiment
from werkzeug.exceptions import BadRequest

MODEL_MAP={
    'project':Project,
    'project_draft':ProjectDraft,
    'sample':Sample,
    'experiment':Experiment
}

def get_stats(model):
    if model not in MODEL_MAP:
        return f"model must be one of {' ,'.join(MODEL_MAP.keys())}",400
    return {model:MODEL_MAP[MODEL_MAP].objects.count()}, 200



def get_model_stats(model, field):
    
    if not model in ['samples', 'experiments']:
        raise BadRequest(description=f"{model} must be sample or experiment")

    db_model = Sample if model == 'samples' else Experiment
    return db_model.objects.item_frequencies(field)
