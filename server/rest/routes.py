from .project import projects_controller
from .experiment import experiments_controller
from .sample import samples_controller
from .draft_project import draft_projects_controller
from .stats import stats_controller

def initialize_routes(api):

	##ADMIN
	# api.add_resource(users_controller.LoginApi, '/api/login')
	# api.add_resource(users_controller.LogoutApi, '/api/logout')


	###DRAFT PROJECT
	api.add_resource(draft_projects_controller.DraftProjectsApi, '/api/draft_projects')
	api.add_resource(draft_projects_controller.DraftProjectApi, '/api/draft_projects/<project_id>')

	###PROJECTS
	api.add_resource(projects_controller.ProjectsApi, '/api/projects')
	api.add_resource(projects_controller.TsvUploadMapApi, '/api/projects/wrangling')
	api.add_resource(projects_controller.ValidateProjectApi, '/api/projects/validate')

	###PROJECT
	api.add_resource(projects_controller.ProjectApi, '/api/projects/<project_id>')
	api.add_resource(projects_controller.ProjectStatsApi, '/api/projects/<project_id>/statistics/<model>/<field>')
	api.add_resource(projects_controller.InferHeaderApi, '/api/projects/<project_id>/match_headers')
	api.add_resource(projects_controller.TsvUploadApi, '/api/projects/<project_id>/upload')
	api.add_resource(projects_controller.LookupProjectDataApi, '/api/projects/<project_id>/lookup')

	###PROJECT SAMPLES
	api.add_resource(samples_controller.SamplesByProjectApi, '/api/projects/<project_id>/samples')
	api.add_resource(samples_controller.SampleByProjectApi, '/api/projects/<project_id>/samples/<sample_id>')

	###PROJECT EXPERIMENTS
	api.add_resource(experiments_controller.ExperimentsByProjectApi, '/api/projects/<project_id>/experiments')
	api.add_resource(experiments_controller.ExperimentByProjectApi, '/api/projects/<project_id>/experiments/<experiment_id>')

	##STATS
	api.add_resource(stats_controller.ModelStatsApi, '/api/statistics/<model>/<field>')

	##SAMPLES
	api.add_resource(samples_controller.SamplesApi, '/api/samples')

	##EXPERIMENTS
	api.add_resource(experiments_controller.ExperimentsApi, '/api/experiments')

	# api.add_resource(experiments_controller.ExperimentsBySampleApi, '/api/projects/<project_id>/samples/<sample_id>/experiments')





