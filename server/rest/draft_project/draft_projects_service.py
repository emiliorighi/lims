from db.models import ProjectDraft,Project
from errors import NotFound
from mongoengine.queryset.visitor import Q
from ..utils import utils

model = ProjectDraft

def get_draft_project(id):
    return utils.return_document_by_id(model, dict(project_id=id))

def create_draft_project(data):
    for req_field in ['project_id', 'name','version']:
        if not data.get(req_field):
            message = f"{req_field} is mandatory in ProjectDraft objects"
            status = 500
            return dict(message=message),status
    if Project.objects(project_id=data['project_id']).first():
        message= f"An existing project with id: {data['project_id']} already exists"
        status = 500
    elif ProjectDraft.objects(project_id=data['project_id']).first():
        message = f"An existing draft project with id: {data['project_id']} already exists"
        status = 500
    else:
        new_draft_project = ProjectDraft(**data)
        new_draft_project.save()
        message = f"Draft project with id: {new_draft_project.project_id} correctly created"
        status = 201
    return dict(message=message),status

def update_draft_project(id, data):
    project_to_update = model.objects(project_id=id)
    project_to_update.update(**data)
    message = f"Draft project {id} correctly updated"
    return dict(message=message), 201


def get_draft_projects(offset=0,limit=20,
                filter=None,sort_order=None):
    if filter:
        projects= model.objects((Q(name__icontains=filter) | Q(name__iexact=filter))).exclude('id','created')
    else:
        projects = model.objects().exclude('id','created')
    if sort_order:
        sort_column = "name"
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        projects = projects.order_by(sort)
    return projects.count(), projects[int(offset):int(offset)+int(limit)]


def delete_draft_project(id):
    project_to_delete = get_draft_project(id)
    project_to_delete.delete()
    message= f"Draft Project with id: {id} successfully deleted"
    return dict(message=message), 201