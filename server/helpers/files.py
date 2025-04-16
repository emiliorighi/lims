import os,hashlib
import json
import csv

FILES_FOLDER = os.getenv('FILES_FOLDER')
#store the file in json lines for scalability
FILE_MAP_PATH = os.path.join(FILES_FOLDER, "hash_map.json")

def read_file_map():
    entries = {}
    if os.path.exists(FILE_MAP_PATH):
        with open(FILE_MAP_PATH,'r') as f:
            entries = json.load(f)
    return entries

def write_file_map(records):
    with open(FILE_MAP_PATH, 'w') as f:
        json.dump(records, f, indent=2)

def update_file_map(hash, filename, project_id, model_name, path):
    hashes_map = read_file_map()
    
    if hash in hashes_map:
        linked_projects = hashes_map[hash]['linked_projects']
        if not project_id in linked_projects:
            linked_projects[project_id] = []
        if not model_name in linked_projects[project_id]:
            linked_projects[project_id].append(model_name)
    else:
        hashes_map[hash] = {
            'filename':filename,
            'path':path,
            'linked_projects':{
                f'{project_id}': [model_name]
            }
        }

    write_file_map(hashes_map)

def delete_file_entry(target_hash):
    records = read_file_map()

    if target_hash in records:
        del records[target_hash]
        write_file_map(records)
        return True

    print(f"Hash {target_hash} not found.")
        
def compute_file_hash(file) -> str:
    hasher = hashlib.sha256()
    for chunk in iter(lambda: file.read(4096), b""):
        hasher.update(chunk)
    file.seek(0)
    return hasher.hexdigest()