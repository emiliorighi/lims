from db.models import File
from werkzeug.exceptions import NotFound
from flask import send_file
import os


def download_protocol(hash):
    protocol = File.objects(hash=hash).first()
    if not protocol:
        raise NotFound(description=f"{hash} not found!")
    file_path = protocol.path
    if not os.path.exists(file_path):
        raise NotFound(description=f"{file_path} not found!")
    return send_file(file_path, as_attachment=True)
