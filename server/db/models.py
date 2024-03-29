import datetime
from .enums import Roles
import mongoengine as db

def handler(event):
    """Signal decorator to allow use of callback functions as class decorators."""
    def decorator(fn):
        def apply(cls):
            event.connect(fn, sender=cls)
            return cls
        fn.apply = apply
        return fn
    return decorator


@handler(db.signals.pre_save)
def create_project_id(sender, document):
    document.project_id =f"{document.name}_{document.version}"

@create_project_id.apply
class Project(db.Document):
    project_id = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField()
    version = db.StringField(required=True)
    experiment = db.DictField(required=True)
    sample = db.DictField(required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    meta = {
        'indexes': [
            'project_id',
            'name',
            '$name',
            ('name','-version')
            ]
    }

class ProjectDraft(db.Document):
    project_id = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField()
    version = db.StringField(required=True)
    experiment = db.DictField()
    sample = db.DictField()
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    valid=db.BooleanField(default=False)
    meta = {
        'indexes': [
            'project_id',
            'name',
            'version'
        ]
    }

class Experiment(db.Document):
    sample_id= db.StringField(required=True)
    experiment_id= db.StringField(unique=True,required=True)
    # user=db.StringField(required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    project=db.StringField(required=True)
    metadata=db.DictField()
    meta = {
        'indexes': ['experiment_id','sample_id']
    }

class File(db.Document):
    id=db.StringField(unique=True,required=True)
    related_object=db.StringField(required=True)
    path=db.StringField(required=True,unique=True)
    metadata=db.DictField()
    meta = {
        'indexes': ['id']
    }

class Analysis(db.Document):
    id = db.StringField(required=True,unique=True)
    experiment = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    user=db.StringField(required=True)
    project=db.StringField(required=True)
    metadata=db.DictField()
    meta = {
        'indexes': [
            'id',
        ],
        'strict': False
    }

class Sample(db.Document):
    created = db.DateTimeField(default=datetime.datetime.utcnow)
    sample_id = db.StringField(required=True)
    taxid = db.StringField()
    scientific_name = db.StringField()
    # user=db.StringField(required=True)
    project=db.StringField(required=True)
    metadata=db.DictField()
    meta = {
        'indexes': [
            'project',
            'sample_id',
            ('project','sample_id')

        ],
        'strict': False
    }

class User(db.Document):
    name=db.StringField(unique=True,required=True)
    password=db.StringField(required=True)
    role=db.EnumField(Roles, required=True)
    projects = db.ListField(db.StringField())

