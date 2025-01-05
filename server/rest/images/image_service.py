from helpers import data
from db.models import Image
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from werkzeug.utils import secure_filename
from flask import send_file
import os


IMAGES_FOLDER = os.getenv('IMAGES_FOLDER')

#get images by project and model and item_id (Do we need a bare images endpoint?)
def get_images(project_id, model, item_id):
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

def download_image(name):

    file_path = os.path.join(IMAGES_FOLDER, name)

    if not os.path.exists(file_path):
        raise NotFound(description=f"{file_path} not found!")
    
    return send_file(file_path, as_attachment=True)

def save_image(request, project_id, model, item_id):

    files = request.files
    if not files or not files.get('protocol'):
        raise BadRequest(description=f"A 'protocol' file is mandatory")
    
    protocol_file = files.get('protocol')
    filename = secure_filename(protocol_file.filename)

    data = request.json if request.is_json else request.form

    description = data.get('description')    

    if project_id:
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

    return f"Protocol {protocol_to_save.name} successfully saved", 201

def delete_image(name):
    # first delete path then object
    file_path = os.path.join(PROTOCOLS_FOLDER, name)
    
    if not os.path.exists(file_path):
        raise NotFound(description=f"{file_path} not found")
    
    os.remove(file_path)

    protocol = get_protocol(name)
    protocol.delete()
    return f"Protocol {name} succesfully deleted", 201