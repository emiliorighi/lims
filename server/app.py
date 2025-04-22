from flask import Flask
from flask_cors import CORS
from config import BaseConfig
from rest import initialize_api
from db.models import User,ResearchProject,ResearchModel,ResearchItem,File,FileLink,User
from db.enums import Roles
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from tendo.singleton import SingleInstance

import os


app = Flask(__name__)

app.config.from_object(BaseConfig)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SAMESITE"] = "None"
app.config["JWT_COOKIE_SECURE"] = True
app.config['CORS_SUPPORTS_CREDENTIALS'] = True

db = MongoEngine()

app.logger.info("Initializing MongoDB")
db.init_app(app)

initialize_api(app)

CORS(app)

jwt = JWTManager(app)

username = os.getenv('DB_USER')
password = os.getenv('DB_PASS')

# File.drop_collection()
# FileLink.drop_collection()
# ResearchProject.drop_collection()
# ResearchModel.drop_collection()
# ResearchItem.drop_collection()
# User.drop_collection()
#create root user if does not exist
try:
    FIRST_START = SingleInstance()
    user = User.objects(name = username).first()
    if not user:
        User(name = username, password = password, role= Roles.ADMIN).save()
except:
    pass
