from db.models import Sample,Experiment


def lookup_project_related_data(project_id):
    response = {}
    response['samples'] = Sample.objects(project=project_id).count()
    response['experiments'] = Experiment.objects(project=project_id).count()
    return response