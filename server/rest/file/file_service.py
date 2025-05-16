from db.models import File, FileLink
from werkzeug.exceptions import NotFound
from flask import send_file
import os
import zipfile
import tempfile


def download_protocol(hash):
    protocol = File.objects(hash=hash).first()
    if not protocol:
        raise NotFound(description=f"{hash} not found!")
    file_path = protocol.path
    if not os.path.exists(file_path):
        raise NotFound(description=f"{file_path} not found!")
    return send_file(file_path, as_attachment=True)

def download_project_model_files(project_id, model_name):
    # Get all file links for the project and model
    links = FileLink.objects(project_id=project_id, model_name=model_name)
    if not links:
        raise NotFound(description=f"No files found for project {project_id} and model {model_name}")

    # Create a temporary zip file
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
        with zipfile.ZipFile(temp_file.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for link in links:
                file = File.objects(hash=link.hash).first()
                if file and os.path.exists(file.path):
                    # Use the link name and extension for the file in the zip
                    zip_path = f"{link.name}.{link.extension}"
                    zipf.write(file.path, zip_path)

        # Return the zip file
        return send_file(
            temp_file.name,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"{project_id}_{model_name}_files.zip"
        )
