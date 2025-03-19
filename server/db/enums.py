from enum import Enum

"""
ROLES:
    - RESEARCHER: READ
    - SAMPLE-MANAGER: CRUD SAMPLE
    - EXPERIMENT-MANAGER: CRUD EXPERIMENT
    - PROJECTS-MANAGAER: CRUD SAMPLE, CRUD EXPERIMENT, ADD-USER TO PROJECT, CR PROJECT
    - ADMIN: CRUD ALL
"""

class Roles(Enum):
    RESEARCHER = 'researcher' ## READ
    MODEL_MANAGER = 'model_manager' ##CRUD MODEL
    PROJECTS_MANAGER = 'project_manager' ##CRUD PROJECT
    ADMIN = 'admin' ##CRUD USERS

class SchemaModel(Enum):
    BIOSAMPLE = 'biosample'
    EXPERIMENT = 'experiment'

class Actions(Enum):
    CREATE= 'created'
    UPDATE='updated'
    DELETE='deleted'

class Model(Enum):
    SAMPLE='sample'
    EXPERIMENT='experiment'
    PROJECT='project'
    USER='user'

class ChartType(Enum):
    BAR="bar"
    LINE="line"
    DOUGHNUT="doughnut"
    PIE="pie"
    HORIZONTAL_BAR="horizontal-bar"

class ChartSize(Enum):
    ONE="1"
    TWO="2"
    THREE="3"
    FOUR="4"