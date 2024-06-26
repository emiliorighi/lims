from flask import Flask
from flask_cors import CORS
from config import BaseConfig
from rest import initialize_api
from db.models import Sample,Project, ProjectDraft
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine



app = Flask(__name__)

app.config.from_object(BaseConfig)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SAMESITE"] = "None"
# app.config["JWT_COOKIE_SECURE"] = True
app.config['CORS_SUPPORTS_CREDENTIALS'] = True

db = MongoEngine()

app.logger.info("Initializing MongoDB")
db.init_app(app)

initialize_api(app)

CORS(app)

jwt = JWTManager(app)

# Project.drop_collection()
# Sample.drop_collection()
# ProjectDraft.drop_collection()


# username = os.getenv('DB_USER')
# password = os.getenv('DB_PASS')

##create root user if does not exist
# try:
#     FIRST_START = SingleInstance()
#     user = BioGenomeUser.objects(name = username).first()
#     cronjobs = CronJob.objects().count()
#     if cronjobs:
#         CronJob.drop_collection()
#     if not user:
#         BioGenomeUser(name = username, password = password, role= Roles.DATA_ADMIN).save()
#     # BioSample.drop_collection()
#     # TaxonNode.drop_collection()
#     # Organism.drop_collection()
#     # LocalSample.drop_collection()
#     # Experiment.drop_collection()
#     # Assembly.drop_collection()
#     # Chromosome.drop_collection()
#     # SampleCoordinates.drop_collection()
#     # GenomeAnnotation.drop_collection()
# except:
#     pass
