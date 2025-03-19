from datetime import datetime
from .enums import Roles, Actions, Model, ChartSize,ChartType
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
def create_model_id(sender, document):
    document.project_id =f"{document.name}_{document.version}"

@create_model_id.apply
class Project(db.Document):
    project_id = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField()
    version = db.StringField(required=True)
    protocols=db.ListField(db.StringField)
    experiment = db.DictField(required=True)
    sample = db.DictField(required=True)
    created = db.DateTimeField(default=datetime.now())
    meta = {
        'indexes': [
            'project_id',
            'name',
            '$name',
            ('name','-version')
            ]
    }

class ResearchProject(db.Document):
    project_id = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField()
    version = db.StringField(required=True)
    models = db.ListField(db.StringField()) ##list of related models
    created = db.DateTimeField(default=datetime.now())
    archived = db.BooleanField(default=False)
    meta = {
        'indexes': [
            'project_id',
            'name',
            '$name',
            ('name','-version')
        ]
    }

class ResearchModel(db.Document):
    created = db.DateTimeField(default=datetime.now())
    project_id = db.StringField(required=True)
    name = db.StringField(required=True)
    fields = db.ListField(db.DictField())
    reference_model = db.StringField()
    description = db.StringField()
    id_format = db.ListField(db.StringField())
    protocols = db.ListField(db.DictField())
    links = db.ListField(db.DictField())
    meta = {
        'indexes': [
            'project_id',
            'name',
            {
                'fields': ['project_id', 'name'],
                'unique': True  # This enforces uniqueness
            }
        ],
        'strict': False
    }

class ResearchItem(db.DynamicDocument):
    created = db.DateTimeField(default=datetime.now())
    item_id = db.StringField(required=True)
    model_name = db.StringField(required=True) #ref to research model
    reference_id = db.StringField()
    project_id = db.StringField(required=True)
    meta = {
        'indexes': [
            'project_id',
            'item_id',
            'model_name',
            {
                'fields': ['project_id', 'item_id', 'model_name'],
                'unique': True  # This enforces uniqueness
            }
        ],
        'strict': False
    }
    
class ProjectDraft(db.Document):
    project_id = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField()
    version = db.StringField(required=True)
    protocols=db.ListField(db.StringField)
    experiment = db.DictField()
    sample = db.DictField()
    created = db.DateTimeField(default=datetime.now())
    meta = {
        'indexes': [
            'project_id',
            'name',
            'version'
        ]
    }

class Experiment(db.DynamicDocument):
    sample_id= db.StringField(required=True)
    experiment_id= db.StringField(required=True)
    created = db.DateTimeField(default=datetime.now())
    project=db.StringField(required=True)
    images=db.ListField(db.StringField)
    protocols=db.ListField(db.StringField)
    meta = {
        'indexes': [
            'project',
            'experiment_id',
            {
                'fields': ['project', 'experiment_id'],
                'unique': True  # This enforces uniqueness
            }
        ],
        'strict': False
    }

class File(db.DynamicDocument):
    file_id=db.StringField(unique=True,required=True)
    related_object=db.StringField(required=True)
    path=db.StringField(required=True,unique=True)
    created = db.DateTimeField(default=datetime.now())
    meta = {
        'indexes': ['file_id', 'path']
    }

class Analysis(db.DynamicDocument):
    id = db.StringField(required=True,unique=True)
    experiment = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.now())
    user=db.StringField(required=True)
    project=db.StringField(required=True)
    files=db.ListField(db.StringField)
    meta = {
        'indexes': [
            'id',
        ],
        'strict': False
    }

class Sample(db.DynamicDocument):
    created = db.DateTimeField(default=datetime.now())
    sample_id = db.StringField(required=True)
    taxid = db.StringField()
    scientific_name = db.StringField()
    project=db.StringField(required=True)
    images=db.ListField(db.StringField)
    protocols=db.ListField(db.StringField)
    meta = {
        'indexes': [
            'project',
            'sample_id',
            {
                'fields': ['project', 'sample_id'],
                'unique': True  # This enforces uniqueness
            }
        ],
        'strict': False
    }

class AuditLog(db.Document):
    user = db.StringField(required=True)  # Store the user's name or ID
    action = db.EnumField(Actions, required=True)  # Store the action performed (create, update, delete)
    model = db.EnumField(Model, required=True)  # Store the model type (Project, Experiment, etc.)
    model_id = db.StringField(required=True)  # Store the ID of the model instance
    timestamp = db.DateTimeField(default=datetime.now, required=True)
    changes = db.DictField()  # Store the details of what was changed
    meta = {
        'indexes': [
            'user',
            'action',
            'model',
            'model_id',
            'timestamp'
        ]
    }

class Chart(db.Document):
    user = db.StringField(required=True)
    project = db.StringField(required=True)
    model = db.EnumField(Model, default=Model.SAMPLE)
    field= db.StringField(required=True)
    chart_type = db.EnumField(ChartType, default=ChartType.HORIZONTAL_BAR)
    size=db.EnumField(ChartSize, default=ChartSize.TWO)

class User(db.Document):
    name=db.StringField(unique=True,required=True)
    password=db.StringField(required=True)
    role=db.EnumField(Roles, required=True)
    projects = db.ListField(db.StringField())
    created = db.DateTimeField(default=datetime.now())
    avatar = db.StringField()


