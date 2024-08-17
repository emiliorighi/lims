from .project import projects_controller
from .draft_project import draft_projects_controller
from .stats import stats_controller
from .project_mapper import project_mapper_controller
from .upload import upload_controller
from .lookup import lookup_controller
from .user import users_controller
from .item import items_controller

def initialize_routes(api):

	##ADMIN
	api.add_resource(users_controller.LoginApi, '/api/login')
	api.add_resource(users_controller.LogoutApi, '/api/logout')

	##APP STATS
	api.add_resource(stats_controller.LookupApi, '/api/lookup')
	
	api.add_resource(stats_controller.ModelStatsApi, '/api/<model>/stats/<field>')

	###DRAFT PROJECT
	api.add_resource(draft_projects_controller.DraftProjectsApi, '/api/draft_projects')
	api.add_resource(draft_projects_controller.DraftProjectApi, '/api/draft_projects/<project_id>')

	### DRAFT PROJECTS ENDPOINT UTILITIES
	api.add_resource(draft_projects_controller.ValidateProjectApi, '/api/draft_projects/validate')
	api.add_resource(draft_projects_controller.TsvUploadMapApi, '/api/draft_projects/map_attributes')

	###PROJECTS
	api.add_resource(projects_controller.ProjectsApi, '/api/projects')
	api.add_resource(projects_controller.ProjectApi, '/api/projects/<project_id>')

	##PROJECT LOOKUP RELATED DATA DATA
	api.add_resource(lookup_controller.LookupProjectDataApi, '/api/projects/<project_id>/lookup')

	#PROJECT ENDPOINT UTILITIES
	api.add_resource(project_mapper_controller.InferHeaderApi, '/api/projects/<project_id>/map_header')
	api.add_resource(upload_controller.TsvUploadApi, '/api/projects/<project_id>/upload_tsv')

	###PROJECT RELATED DATA
	api.add_resource(items_controller.ItemsByProjectApi, '/api/projects/<project_id>/<model>')
	api.add_resource(items_controller.ModelByProjectStatsApi, '/api/projects/<project_id>/<model>/stats/<field>')
	api.add_resource(items_controller.ItemByProjectApi, '/api/projects/<project_id>/<model>/<item_id>')

	##SAVED CHARTS MANAGEMENT 
	# api.add_resource(stats_controller.ModelStatsApi, '/api/charts', 'api/charts/<chart_id>')





