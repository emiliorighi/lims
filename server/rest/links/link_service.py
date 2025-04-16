from helpers import data, files as file_helper, links as link_helper, user as user_helper
from db.models import File, FileLink
from mongoengine.queryset.visitor import Q
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from werkzeug.utils import secure_filename
import os

FILE_FOLDER = os.getenv('FILES_FOLDER')
TSV_FIELDS = ['name', 'description', 'project_id', 'model_name', 'path']

def upload_links(project_id, model_name, files, metadata):
        user = user_helper.get_current_user()
        for index, file in enumerate(files):
            try:
                name, description, type = link_helper.process_payload(metadata, index)
                if not all([name, type]):
                    raise BadRequest(description=f"Name or type of {file.filename} is/are missing")
    
                upload_link(project_id, model_name, file, name, type, user.name, description)

            except Exception as e:
                raise BadRequest(description=f"Error processing file {file.filename}: {str(e)}")

        return {"message": "Files uploaded"}


#TODO: add file lock to avoid concurrency in tsv writing
def upload_link(project_id, model_name, file, name, type,username, description=None):

    query = link_helper.create_link_query(project_id, model_name, name, type)

    if FileLink.objects(**query).first():
        raise Conflict(description=f"A {type} with name {name} already exists in {model_name} of {project_id}")
    
    ##process and store file
    filename = secure_filename(file.filename)
    file_hash = file_helper.compute_file_hash(file)
    storage_path, ext = save_link(file, file_hash, filename)

    # save link to project/model
    FileLink(
        hash=file_hash,
        name=name,
        description=description,
        created_by=username,
        extension=ext,
        model_name=model_name,
        project_id=project_id,
        type=type
    ).save()

    file_helper.update_file_map(file_hash, name, project_id, model_name, storage_path)
    return f"Protocol {name} created"

def get_links(args):
    query = { **args}
    q_query = None
    filter = query.pop('filter', None)
    format = query.pop('format', 'json')

    if filter:
        q_query = Q(name__icontains=filter) | Q(name__iexact=filter) | Q(description__icontains=filter) | Q(description__icontains=filter)
    
    limit, offset = data.get_pagination(query)
    sort_column, sort_order = data.get_sort(query)

    query_set, q_query = data.create_query(query, q_query)
    cursor = FileLink.objects(**query_set)
    print(query_set)
    print(cursor.count())
    if q_query:
        cursor = cursor.filter(q_query)
    
    if sort_column and sort_order:
        cursor = data.apply_sorting(cursor, sort_column, sort_order)
    
    return data.generate_response(format, TSV_FIELDS, cursor, limit, offset)    

def get_project_model_links(project_id, model_name, args):
    query = {**data.project_model_query(project_id, model_name), **args}
    return get_links(query)
    
def save_link(file, hash, filename):
    ext = os.path.splitext(filename)[1].lower().lstrip(".")
    hash_prefix = hash[:2]
    storage_dir = os.path.join(FILE_FOLDER, hash_prefix)
    os.makedirs(storage_dir, exist_ok=True)

    storage_filename = f"{hash}.{ext}"
    storage_path = os.path.join(storage_dir, storage_filename)
    protocol = File.objects(hash=hash).first()
    if not protocol:
        # Save file to disk
        file.save(storage_path)
        # Create protocol metadata
        protocol = File(
            original_filename=filename,
            hash=hash,
            extension=ext,
            content_type=file.content_type,
            path=storage_path,
        )
        protocol.save()
    return storage_path, ext

def delete_unbound_file(hash):
    if FileLink.objects(hash=hash).count():
        return
    
    file_to_delete = File.objects(hash=hash).first()
    storage_path = file_to_delete.path
    try:

        # Step 1: Delete the file
        if os.path.isfile(storage_path):
            os.remove(storage_path)

        # Step 2: Delete parent dirs if empty 
        dir_path = os.path.dirname(storage_path)
        base_dir = os.path.abspath(FILE_FOLDER)  

        while os.path.abspath(dir_path).startswith(base_dir):
            try:
                os.rmdir(dir_path)  # removes dir only if empty
                dir_path = os.path.dirname(dir_path)  # go one level up
            except OSError:
                break  # Directory not empty or cannot be removed

        file_helper.delete_file_entry(hash)
        file_to_delete.delete()
    except Exception as e:
        print(f"Error while deleting protocol file or directory: {e}")

def delete_link(project_id, model_name, name, type):
    query = data.project_model_query(project_id, model_name)
    query['type'] = type
    query['name'] = name
    link_to_delete = FileLink.objects(project_id=project_id, model_name=model_name, name=name).first()
    if not link_to_delete:
        raise NotFound(description=f"Link {name} not found for {model_name} of {project_id}")
    
    hash = link_to_delete.hash
    link_to_delete.delete()
    #handle protocol_storage
    delete_unbound_file(hash)

    return f"Protocol {name} succesfully deleted"