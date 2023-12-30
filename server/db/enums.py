from enum import Enum

class Roles(Enum):
    RESEARCHER = 'researcher' 
    SAMPLE_MANAGER = 'sample_manager'
    EXPERIMENT_MANAGER = 'experiment_manager'
    DATA_MANAGER = 'data_manager'
    ADMIN = 'admin'

class SchemaModel(Enum):
    BIOSAMPLE = 'biosample'
    EXPERIMENT = 'experiment'