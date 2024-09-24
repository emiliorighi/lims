import http from "../../http";

const { base, yaml } = http

class ProjectService {

  getProjects(params) {
    return base.get('/projects', { params: params })
  }
  getProject(id) {
    return base.get(`/projects/${id}`)
  }
  getProjectStats(id, model, field) {
    return base.get(`/projects/${id}/${model}/stats/${field}`)
  }
  lookupProject(id) {
    return base.get(`/projects/${id}/lookup`)
  }
  validateYAMLProject(data) {
    return yaml.post('/draft_projects/validate', data)
  }
  validateJSONProject(data) {
    return base.post('/draft_projects/validate', data)
  }
  inferAttributesProject(data) {
    return base.post('/draft_projects/map_attributes', data)
  }
  inferHeadersFromTSV(projectId, data) {
    return base.post(`/projects/${projectId}/map_header`, data)
  }
  getDraftProjects(params) {
    return base.get('/draft_projects', { params: params })
  }
  getDraftProject(id) {
    return base.get(`/draft_projects/${id}`)
  }
  getUserProjects(name, params){
    return base.get(`/users/${name}/projects`, {params: params})
  }
}

export default new ProjectService();
