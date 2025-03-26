from .stats import stats_controller
from .project_mapper import project_mapper_controller
from .upload import upload_controller
from .lookup import lookup_controller
from .user import users_controller
from .item import items_controller
from .research_project import research_projects_controller
from .research_models import model_controller

def initialize_routes(api):

	##ADMIN
	api.add_resource(users_controller.LoginApi, '/api/login')
	api.add_resource(users_controller.LogoutApi, '/api/logout')

	##PROTOCOLS
	# api.add_resource(protocol_controller.ProtocolsAPI, '/api/protocols')
	# api.add_resource(protocol_controller.ProtocolAPI, '/api/protocols/<name>')

	##APP STATS
	api.add_resource(stats_controller.LookupApi, '/api/lookup')

	##USERS
	api.add_resource(users_controller.UsersApi, '/api/users', '/api/users/<name>')
	api.add_resource(users_controller.UserProjectsApi, '/api/users/<name>/projects')

	###PROJECTS
	api.add_resource(research_projects_controller.ResearchProjectsApi, '/api/projects')
	api.add_resource(research_projects_controller.ResearchProjectApi, '/api/projects/<project_id>')

	##PROJECT SCHEMA
	api.add_resource(research_projects_controller.ResearchProjectSchema, '/api/projects/<project_id>/schema')

	## PROJECT STATS
	api.add_resource(lookup_controller.LookupProjectDataApi, '/api/projects/<project_id>/lookup')

	## PROJECT MODELS
	api.add_resource(model_controller.ModelsApi, '/api/projects/<project_id>/models')
	api.add_resource(model_controller.ModelApi, '/api/projects/<project_id>/models/<model_name>')
	api.add_resource(stats_controller.ModelStatsApi, '/api/projects/<project_id>/models/<model_name>/stats/<field>')


	api.add_resource(items_controller.ItemsByProjectModelApi, '/api/projects/<project_id>/models/<model_name>/records')
	api.add_resource(items_controller.ItemByProjectModelApi, '/api/projects/<project_id>/models/<model_name>/records/<record_id>')
	api.add_resource(items_controller.RelatedItemsByProjectModelApi, '/api/projects/<project_id>/models/<model_name>/records/<record_id>/related_records')

	##PROJECT LOOKUP RELATED DATA

	##PROJECT RELATED PROTOCOLS
	# api.add_resource(protocol_controller.ProtocolsAPI, '/api/projects/<project_id>/protocols')
	# api.add_resource(protocol_controller.ProtocolAPI, '/api/projects/<project_id>/protocols/<name>')
	# api.add_resource(protocol_controller.DownloadProtocolAPI, '/api/projects/<project_id>/protocols/<name>/download')

	#PROJECT ENDPOINT UTILITIES
	api.add_resource(project_mapper_controller.InferHeaderApi, '/api/projects/<project_id>/map_header')
	api.add_resource(upload_controller.TsvUploadApi, '/api/projects/<project_id>/upload')

	###ALL ITEMS ENDPOINT
	api.add_resource(items_controller.ItemsApi, '/api/items')



	# DO WE NEED THIS ENDPOINT?
	# api.add_resource(items_controller.ItemByProjectModelApi, '/api/projects/<project_id>/<model>/<item_id>/protocols')

	# api.add_resource(items_controller.ItemByProjectModelApi, '/api/projects/<project_id>/<model>/<item_id>/images')
	# api.add_resource(items_controller.ItemByProjectModelApi, '/api/projects/<project_id>/<model>/<item_id>/images/<name>/download')



	api.add_resource(items_controller.ModelByProjectStatsApi, '/api/projects/<project_id>/<model>/stats/<field>')

	##SAVED CHARTS MANAGEMENT 
	# api.add_resource(stats_controller.ModelStatsApi, '/api/charts', 'api/charts/<chart_id>')





