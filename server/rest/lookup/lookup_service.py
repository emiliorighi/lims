from db.models import ResearchItem,ResearchModel


def lookup_project_related_data(project_id):
    models = ResearchModel.objects(project_id=project_id).scalar('name')
    response = {}
    for model in models:
        response[model] = ResearchItem.objects(project_id=project_id, model_name=model).count()
    return response