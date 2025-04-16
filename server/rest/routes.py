from .stats import stats_controller
from .upload import upload_controller
from .lookup import lookup_controller
from .user import users_controller
from .record import records_controller
from .project import projects_controller
from .research_models import model_controller
from .file import file_controller
from .links import link_controller

def initialize_routes(api):
    api_prefix = '/api'

    ## AUTH
    auth_routes = [
        (users_controller.LoginApi, '/auth/login'),
        (users_controller.LogoutApi, '/auth/logout'),
    ]

    ## USERS
    user_routes = [
        (users_controller.UsersApi, '/users', '/users/<name>'),
        (users_controller.UserProjectsApi, '/users/<name>/projects'),
    ]

    ## GLOBAL STATS / LOOKUP
    global_routes = [
        (stats_controller.LookupApi, '/lookup'),
        (file_controller.FileAPI, '/files/<hash>/download')
    ]

    ## PROJECTS
    project_routes = [
        (projects_controller.ResearchProjectsApi, '/projects'),
        (projects_controller.ResearchProjectApi, '/projects/<project_id>'),
        (projects_controller.ArchiveResearchProjectApi, '/projects/<project_id>/archive'),
        (projects_controller.UnarchiveResearchProjectApi, '/projects/<project_id>/unarchive'),
        (projects_controller.ResearchProjectSchema, '/projects/<project_id>/schema'),
        (lookup_controller.LookupProjectDataApi, '/projects/<project_id>/lookup'),
        (upload_controller.TsvUploadApi, '/projects/<project_id>/upload'),
    ]

    ## MODELS
    model_routes = [
        (model_controller.ModelsApi, '/models'),
        (model_controller.ProjectModelsApi, '/projects/<project_id>/models'),
        (model_controller.ProjectModelApi, '/projects/<project_id>/models/<model_name>'),
        (lookup_controller.LookupModelDataApi, '/projects/<project_id>/models/<model_name>/lookup'),
        (stats_controller.ModelStatsApi, '/projects/<project_id>/models/<model_name>/stats/<field>'),
        (records_controller.ModelByProjectStatsApi, '/projects/<project_id>/<model>/stats/<field>'),
    ]

    ## RECORDS
    record_routes = [
        (records_controller.ItemsApi, '/records'),
        (stats_controller.RecordStatsApi, '/records/stats/<field>'),
        (records_controller.ItemsByProjectModelApi, '/projects/<project_id>/models/<model_name>/records'),
        (records_controller.ItemByProjectModelApi, '/projects/<project_id>/models/<model_name>/records/<record_id>'),
        (records_controller.RelatedItemsByProjectModelApi, '/projects/<project_id>/models/<model_name>/records/<record_id>/related_records'),
    ]
    link_routes = [
        (link_controller.LinksAPI, '/links'),
        (stats_controller.LinkStatsApi, '/links/stats/<field>'),
        (link_controller.ProjectModelLinksAPI, '/projects/<project_id>/models/<model_name>/links'),
        (link_controller.ProjectModelLinkAPI, '/projects/<project_id>/models/<model_name>/links/<type>/<name>'),
    ]


    # Combine all route groups
    all_routes = (
        auth_routes + user_routes + global_routes +
        project_routes + model_routes + record_routes +
        link_routes
    )

    # Register all routes with prefix
    for resource, *paths in all_routes:
        api.add_resource(resource, *(api_prefix + path for path in paths))




