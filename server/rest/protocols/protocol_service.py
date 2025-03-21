from helpers import data
from db.models import Protocol, Experiment, Sample
from ..project import projects_service
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from werkzeug.utils import secure_filename
from flask import send_file
import os


PROTOCOLS_FOLDER = os.getenv('PROTOCOLS_FOLDER')

def get_protocols_by_project(project_id, args):
    #check if project exist
    projects_service.get_project(project_id)
    cursor = Protocol.objects(project_id=project_id)
    filter = args.get('filter')
    if filter:
        q = Q(name__icontains=filter) | Q(name__iexact=filter) | Q(description__icontains=filter) | Q(description__icontains=filter)
        cursor = cursor.filter(q)

    sort_column, sort_order = data.get_sort(args)
    if sort_column and sort_order:
        cursor = data.apply_sorting(cursor, sort_column, sort_order)

    limit, offset = data.get_pagination(args)

    total = cursor.count()
    response = {'total': total, 'data': list(cursor.skip(offset).limit(limit).as_pymongo())}
    return data.dump_json(response), "application/json", 200

def get_protocols(args):
    cursor = Protocol.objects()
    filter = args.get('filter')
    if filter:
        q = Q(name__icontains=filter) | Q(name__iexact=filter) | Q(description__icontains=filter) | Q(description__icontains=filter)
        cursor = cursor.filter(q)

    sort_column, sort_order = data.get_sort(args)
    if sort_column and sort_order:
        cursor = data.apply_sorting(cursor, sort_column, sort_order)

    limit, offset = data.get_pagination(args)

    total = cursor.count()
    response = {'total': total, 'data': list(cursor.skip(offset).limit(limit).as_pymongo())}
    return data.dump_json(response), "application/json", 200

def get_protocol(name):
    protocol = Protocol.objects(name=name).first()
    if not protocol:
        raise NotFound(description=f"{name} not found!")
    return protocol

def download_protocol(name):

    file_path = os.path.join(PROTOCOLS_FOLDER, name)

    if not os.path.exists(file_path):
        raise NotFound(description=f"{file_path} not found!")
    
    return send_file(file_path, as_attachment=True)


def save_protocol(request, project_id=None):
    project = None
    files = request.files
    if not files or not files.get('protocol'):
        raise BadRequest(description=f"A 'protocol' file is mandatory")
    
    protocol_file = files.get('protocol')
    filename = secure_filename(protocol_file.filename)

    data = request.json if request.is_json else request.form

    description = data.get('description')    

    if project_id:
        project = projects_service.get_project(project_id)
        if not project:
            raise NotFound(description=f"Project {project_id} not found! Does the project exists?")
        filename = f"{project_id}_{filename}"

    existing_protocol = Protocol.objects(name=filename).first()
    if existing_protocol:
        raise Conflict(description=f"A protocol with name: {filename} already exists")
    
    files = request.files
    if not files or not files.get('protocol'):
        raise BadRequest(description=f"A 'protocol' file is mandatory")
    
    protocol_file = files.get('protocol')
    filename = secure_filename(protocol_file.filename)

    folder = f"/{PROTOCOLS_FOLDER}"
    #first create file
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(PROTOCOLS_FOLDER, filename)
    if os.path.exists(file_path):
        raise Conflict(description=f"A protocol file with path {file_path} already exists")

    protocol_file.save(file_path)

    protocol_to_save = Protocol(**{
        'name': filename,
        'description': description,
        'project_id': project_id,
    })

    protocol_to_save.save()

    ## add protocol to project
    if project:
        project.modify(add_to_set__protocols=filename)

    return f"Protocol {protocol_to_save.name} successfully saved", 201

def delete_protocol(name):
    # first delete path then object
    file_path = os.path.join(PROTOCOLS_FOLDER, name)

    if not os.path.exists(file_path):
        raise NotFound(description=f"{file_path} not found")
    
    os.remove(file_path)

    protocol = get_protocol(name)

    if protocol.project_id:
        #update project and related data
        project = projects_service.get_project(protocol.project_id)
        project.modify(pull__protocols=name)

    
    
    protocol.delete()
    return f"Protocol {name} succesfully deleted", 201