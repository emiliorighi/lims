from db.models import ProjectDraft,Project
from mongoengine.queryset.visitor import Q
from ..utils import utils
from werkzeug.exceptions import NotFound


def get_draft_project(project_id):
    draft_projects=utils.get_documents_by_query(ProjectDraft, dict(project_id=project_id),('id','created','valid'))
    if draft_projects.first():
        return draft_projects.as_pymongo()[0]
    raise NotFound(description=f"Draft Project: {project_id} not found!")

def create_draft_project(data):
    for req_field in ['project_id', 'name','version']:
        if not data.get(req_field):
            message = f"{req_field} is mandatory in ProjectDraft objects"
            status = 400
            return [message],status
    if Project.objects(project_id=data['project_id']).first():
        message= f"An existing project with id: {data['project_id']} already exists"
        status = 409
    elif ProjectDraft.objects(project_id=data['project_id']).first():
        message = f"An existing draft project with id: {data['project_id']} already exists"
        status = 409
    else:
        new_draft_project = ProjectDraft(**data)
        new_draft_project.save()
        message = f"Draft project with id: {new_draft_project.project_id} correctly created"
        status = 201
    return [message],status

def update_draft_project(project_id, data):
    projects_to_update = utils.get_documents_by_query(ProjectDraft, dict(project_id=project_id))
    if not projects_to_update.first():
        raise NotFound(description=f"Draft Projects: {project_id} not found!")
    projects_to_update.update_one(**data)
    message = f"Draft project {project_id} correctly updated"
    return [message], 201


def get_draft_projects(offset=0,limit=20,
                filter=None,sort_order=None):
    if filter:
        projects= ProjectDraft.objects((Q(name__icontains=filter) | Q(name__iexact=filter))).exclude('id','created')
    else:
        projects = ProjectDraft.objects().exclude('id','created')
    if sort_order:
        sort_column = "name"
        sort = '-'+sort_column if sort_order == 'desc' else sort_column
        projects = projects.order_by(sort)
    return projects.count(), projects[int(offset):int(offset)+int(limit)]


def delete_draft_project(project_id):
    project_to_delete=utils.get_documents_by_query(ProjectDraft,dict(project_id=project_id)).first()
    if not project_to_delete:
        raise NotFound(description=f"Draft Projects: {project_id} not found!")
    project_to_delete.delete()
    message= f"Draft Project with id: {project_id} successfully deleted"
    return [message], 201