from db.models import Project
from errors import NotFound
from mongoengine.queryset.visitor import Q



def get_project(id):
    project = Project.objects(project_id=id).exclude('id').first()
    if not project:
        raise NotFound
    return project

def get_projects(offset=0,limit=20,
                filter=None,sort_order=None):
    if filter:
        projects= Project.objects((Q(name__icontains=filter) | Q(name__iexact=filter))).exclude('id','created')
    else:
        projects = Project.objects().exclude('id','created')
    if sort_order:
        sort_column = "name"
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        projects = projects.order_by(sort)
    return projects.count(), projects[int(offset):int(offset)+int(limit)]


# def download_yaml_schema(project):

# def upload_yaml_schema(payload, file=None):