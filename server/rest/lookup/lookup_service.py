from db.models import ResearchItem, ResearchModel, FileLink
from helpers import data as data_helper

def lookup_project_related_data(project_id):
    models = ResearchModel.objects(project_id=project_id).scalar('name')
    response = {}
    for model in models:
        response[model] = ResearchItem.objects(project_id=project_id, model_name=model).count()
    return response

def lookup_model_related_data(project_id, model_name):
    query = data_helper.project_model_query(project_id, model_name)
    lookup_dict = {
        'records': ResearchItem.objects(**query).count()
    }
    for file_type in ['images', 'protocols', 'analysis']:
        lookup_dict[file_type] = FileLink.objects(type=file_type, **query).count()
    #
    return lookup_dict