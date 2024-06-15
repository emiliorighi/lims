from .project import projects_controller
from .experiment import experiments_controller
from .sample import samples_controller
from .draft_project import draft_projects_controller

def initialize_routes(api):

	##ADMIN
	# api.add_resource(users_controller.LoginApi, '/api/login')
	# api.add_resource(users_controller.LogoutApi, '/api/logout')

	api.add_resource(projects_controller.ProjectsApi, '/api/projects')

	api.add_resource(projects_controller.TsvUploadApi, '/api/projects/wrangling')

	api.add_resource(projects_controller.ValidateProjectApi, '/api/projects/validate')

	api.add_resource(projects_controller.ProjectApi, '/api/projects/<project_id>')
	
	api.add_resource(projects_controller.LookupProjectDataApi, '/api/projects/<project_id>/lookup')


	api.add_resource(samples_controller.SamplesApi, '/api/projects/<project_id>/samples')
	api.add_resource(samples_controller.SamplesUploadApi, '/api/projects/<project_id>/samples/upload')

	api.add_resource(samples_controller.SampleApi, '/api/projects/<project_id>/samples/<sample_id>')
	api.add_resource(experiments_controller.ExperimentsBySampleApi, '/api/projects/<project_id>/samples/<sample_id>/experiments')

	api.add_resource(experiments_controller.ExperimentsApi, '/api/projects/<project_id>/experiments')
	# api.add_resource(experiments_controller.ExperimentsApi, '/api/projects/<project_id>/experiments/upload')
	api.add_resource(experiments_controller.ExperimentApi, '/api/projects/<project_id>/experiments/<experiment_id>')



	api.add_resource(draft_projects_controller.DraftProjectsApi, '/api/draft_projects')
	api.add_resource(draft_projects_controller.DraftProjectApi, '/api/draft_projects/<project_id>')

	# api.add_resource(uploads_controller.ExcelParserApi, '/api/spreadsheet_upload')
	
	# api.add_resource(reports_controller.ReportsApi,'/api/reports',)
	# api.add_resource(reports_controller.ReportApi,'/api/reports/<id>',)
	# ##BIOSAMPLES
	# api.add_resource(samples_controller.SamplesApi, '/api/biosamples')
	# api.add_resource(samples_controller.SampleApi, '/api/biosamples/<id>')
	# api.add_resource(samples_controller.SampleRelatedExperiments, '/api/biosamples/<id>/experiments') 


	# ##READS (Experiment Document in DB)
	# api.add_resource(experiments_controller.ExperimentRelatedAnalysis, '/api/experiments/<id>/analysis') 
	# api.add_resource(experiments_controller.ExperimentApi, '/api/experiments/<id>')
	# api.add_resource(experiments_controller.ExperimentsApi, '/api/experiments')

	# ##USERS
	# api.add_resource(users_controller.UsersApi, '/api/users')
	# api.add_resource(users_controller.UserApi,'/api/users/<id>')
	# api.add_resource(users_controller.UserApi,'/api/users/<id>/experiments')
	# api.add_resource(users_controller.UserApi,'/api/users/<id>/samples')
	# api.add_resource(users_controller.UserApi,'/api/users/<id>/analysis')



	# ##STATS TODO: IMPROVE IT.. 
	# api.add_resource(stats_controller.StatsApi,'/api/stats')
	# api.add_resource(stats_controller.FieldStatsApi, '/api/stats/<model>')



