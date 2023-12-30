from .user import users_controller
# from .sample import samples_controller
# from .experiment import experiments_controller
# from .stats import stats_controller
# from .upload import uploads_controller
# from .report import reports_controller
from .project import projects_controller
def initialize_routes(api):

	##ADMIN
	# api.add_resource(users_controller.LoginApi, '/api/login')
	# api.add_resource(users_controller.LogoutApi, '/api/logout')

	api.add_resource(projects_controller.ProjectsApi, '/api/projects')
	api.add_resource(projects_controller.ProjectApi, '/api/projects/<id>')



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



