from db.models import Project,ProjectDraft,Sample,Experiment
from werkzeug.exceptions import BadRequest,NotFound

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

def get_project_stats(project_id, model, field):
    
    project = Project.objects(project_id=project_id).exclude('id').first()
    if not project:
        raise NotFound(description=f"Project: {project_id} not found!")
    
    if not model in ['sample', 'experiment']:
        raise BadRequest(description=f"{model} must be sample or experiment")

    db_model = Sample if model == 'sample' else Experiment
    return db_model.objects(project=project_id).item_frequencies(f"metadata.{field}")


def get_model_stats(model, field):
    
    if not model in ['samples', 'experiments']:
        raise BadRequest(description=f"{model} must be sample or experiment")

    db_model = Sample if model == 'samples' else Experiment
    return db_model.objects.item_frequencies(field)
