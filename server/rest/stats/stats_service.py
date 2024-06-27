from db.models import Project,ProjectDraft,Sample,Experiment

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