from datetime import datetime
from .enums import Roles, Actions, LinkType, DocumentTypes
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

class ResearchProject(db.Document):
    project_id = db.StringField(required=True, unique=True)
    name = db.StringField(required=True)
    description = db.StringField()
    version = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.now())
    archived = db.BooleanField(default=False)
    created_by = db.StringField()
    meta = {
        'indexes': [
            'project_id',
            'name',
            '$name',
            ('name','-version'),
                        {
                'fields': ['project_id', 'name'],
                'unique': True  # This enforces uniqueness
            }
        ],
        'strict': False
    }

class ResearchModel(db.Document):
    created = db.DateTimeField(default=datetime.now())
    project_id = db.StringField(required=True)
    name = db.StringField(required=True)
    fields = db.ListField(db.DictField())
    reference_model = db.StringField()
    inherit_reference_id = db.BooleanField(default=False)
    description = db.StringField()
    id_format = db.ListField(db.StringField())
    created_by = db.StringField()
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
    created_by = db.StringField()
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
    
class File(db.Document):
    original_filename = db.StringField(required=True)
    hash = db.StringField(required=True, unique=True)
    extension = db.StringField(required=True)
    content_type = db.StringField()
    path = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.now())
    meta = {
        'indexes': [
            'hash',
            'original_filename',
        ]
    }
## project-model link to protocol
class FileLink(db.DynamicDocument):
    hash = db.StringField(required=True) #ref to file hash
    model_name = db.StringField(required=True)
    project_id = db.StringField(required=True)
    name = db.StringField(required=True)
    extension = db.StringField()
    description = db.StringField()
    created = db.DateTimeField(default=datetime.now())
    type = db.EnumField(LinkType, required=True)
    created_by = db.StringField()
    meta = {
        'indexes': [
            'hash',
            'name',
            'project_id',
            'model_name',
            {
                'fields': ['project_id', 'model_name', 'name', 'type'],
                'unique': True  # This enforces uniqueness
            }
        ]
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

class Chart(db.Document):
    user = db.StringField(required=True)
    project_id = db.StringField(required=True)
    model_name = db.StringField(required=True)
    field= db.StringField(required=True)
    chart_type = db.StringField()

class User(db.Document):
    name=db.StringField(unique=True,required=True)
    password=db.StringField(required=True)
    role=db.EnumField(Roles, required=True)
    projects = db.ListField(db.StringField())
    created = db.DateTimeField(default=datetime.now())
    avatar = db.StringField()

class AuditLog(db.Document):
    user = db.StringField(required=True)  # Store the user's name or ID
    action = db.EnumField(Actions, required=True)  # Store the action performed
    document_type = db.EnumField(DocumentTypes, required=True)  # Type of document being modified
    document_id = db.StringField(required=True)  # ID of the specific document
    project_id = db.StringField(required=True)  # Project context
    previous_object = db.DictField()  # Previous state of the document
    new_object = db.DictField()  # New state of the document
    changes = db.DictField()  # Specific changes made (for updates)
    metadata = db.DictField()  # Additional context (e.g., file size for uploads)
    timestamp = db.DateTimeField(default=datetime.now)
    
    meta = {
        'indexes': [
            'user',
            'action',
            'document_type',
            'document_id',
            'project_id',
            'timestamp',
            {'fields': ['project_id', 'document_type']},  # Compound index for project-specific queries
            {'fields': ['document_type', 'document_id']}  # Compound index for document history
        ]
    }


