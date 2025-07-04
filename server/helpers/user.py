from db.models import User
from werkzeug.exceptions import Unauthorized,NotFound
from flask_jwt_extended import get_jwt

def get_current_user():
    try:
        claims = get_jwt()
        username = claims.get('username')
    except Exception as e:
        print(e)
        raise Unauthorized(description="Authenticate first")
    user = User.objects(name=username).first()
    if not user:
        raise NotFound(description="User not found")
    return user
