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
    SAMPLE_MANAGER = 'sample_manager'
    EXPERIMENT_MANAGER = 'experiment_manager'
    PROJECTS_MANAGER = 'project_manager'
    ADMIN = 'admin'



# class AccessRights(Enum):
#     READ
#     CREATE
class SchemaModel(Enum):
    BIOSAMPLE = 'biosample'
    EXPERIMENT = 'experiment'