

def create_link_query(project_id, model_name, name, type):
    return dict(project_id=project_id, model_name=model_name,name=name, type=type)

def process_payload(metadata, idx):
    name = metadata.get(f"metadata[{idx}][name]", [None])[0]
    description = metadata.get(f"metadata[{idx}][description]", [""])[0]
    type = metadata.get(f"metadata[{idx}][type]", [""])[0]
    return name,description,type