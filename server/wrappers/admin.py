from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from functools import wraps
from flask import Response
import json

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("sub").get("role")
            if role and role == "admin":
                return fn(*args, **kwargs)
            else:
                return Response(json.dumps(dict(message="Admins only!")), mimetype="application/json", status=403)
        return decorator

    return wrapper



