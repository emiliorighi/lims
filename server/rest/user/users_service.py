from db.models import User,Project
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from mongoengine.errors import NotUniqueError

FIELDS_TO_EXCLUDE=['password','id','created']

def get_users(offset=0,limit=20,
                filter=None, project=None):
    
    users = User.objects().exclude(*FIELDS_TO_EXCLUDE)
    if project:
        users = users.filter(projects=project)
    if filter:
        users = users.filter(Q(name__iexact=filter) | Q(name__icontains=filter))
    return users.count(), users[int(offset):int(offset)+int(limit)]

def create_user(data):

    req_attrs=['name','password']
    missing_attrs=[k for k in req_attrs if not data.get(k)]
    if missing_attrs:
        raise BadRequest(description=f"{' '.join(missing_attrs)} is/are mandatory")

    name = data.get('name')
    
    projects = data.get('projects',[])

    existing_projects = Project.objects(project_id__in=projects).scalar('project_id')
    for project in projects:
        if project not in existing_projects:
            raise BadRequest(description=f"{project} not found")

    try:
        User(**data).save()

    except NotUniqueError as e:
        raise Conflict(description=f"{name} already exists")

    except Exception as e:
        raise BadRequest(description=f"Error: {e}")

    return f'{name} correctly created', 201

def update_user(name, data):
    ex_user = User.objects(name=name).first()
    if not ex_user:
        raise NotFound(description=f"{name} not found")
    
    projects = data.get('projects',[])
    existing_projects = Project.objects(project_id__in=projects).scalar('project_id')
    for project in projects:
        if project not in existing_projects:
            raise BadRequest(description=f"{project} not found")
    try:
        ex_user.update(**data)
    except Exception as e:
        raise BadRequest(description=f"Error: {e}")
    
    return f'{name} correctly updated', 201

def delete_user(name):
    ex_user = User.objects(name=name).first()
    if not ex_user:
        raise NotFound(description=f"{name} not found")
    try:
        ex_user.delete()
    except Exception as e:
        raise BadRequest(description=f"Error: {e}")
    
    return f'{name} correctly deleted', 201

def get_user(name):
    user = User.objects(name=name).first()
    if not user:
        raise NotFound(description=f"{name} not found")
    return user
    
def login_user(data):
    req_fields = ['name','password']
    missing_fields = [k for k in req_fields if not data.get(k)]
    if missing_fields:
        raise BadRequest(description=f"{' '.join(missing_fields)} is/are mandatory")
    
    name = data.get('name')
    pwd = data.get('password')

    user = User.objects(name=name, password=pwd).exclude('id','created','password').as_pymongo()
    if not user or not user[0]:
        raise BadRequest(description="Wrong name or password")
    return user[0]
