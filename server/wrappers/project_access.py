from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from functools import wraps
from flask import Response
import json
from db.models import User

def project_access_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            project_id = kwargs.get('project_id')
            verify_jwt_in_request()
            claims = get_jwt()
            username = claims.get("username")
            role = claims.get("role")
            user = User.objects(name=username).first()
            if not user:
                return Response(json.dumps(dict(message=f"User {username} not found")), mimetype="application/json", status=403)

            if role == 'admin' or project_id in user.projects:
                return fn(*args, **kwargs)
            else:
                return Response(json.dumps(dict(message="You don't have access to this project")), mimetype="application/json", status=403)

        return decorator

    return wrapper

