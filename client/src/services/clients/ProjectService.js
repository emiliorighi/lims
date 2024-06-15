import http from "../../http";

const { base, yaml } = http

class ProjectService {

  getProjects(params) {
    return base.get('/projects', { params: params })
  }
  getProject(id) {
    return base.get(`/projects/${id}`)
  }
  lookupProject(id) {
    return base.get(`/projects/${id}/lookup`)
  }
  createProject(data) {
    return base.post('/projects', data)
  }
  validateYAMLProject(data) {
    return yaml.post('/projects/validate', data)
  }
  validateJSONProject(data) {
    return base.post('/projects/validate', data)
  }
  inferAttributesProject(data){
    return base.post('/projects/wrangling', data)
  }
  getDraftProjects(params) {
    return base.get('/draft_projects', { params: params })
  }
  getDraftProject(id) {
    return base.get(`/draft_projects/${id}`)
  }
  createDraftProject(data) {
    return base.post('/draft_projects', data)
  }
  updateDraftProject(id, data){
    return base.put(`/draft_projects/${id}`, data)
  }
}

export default new ProjectService();
