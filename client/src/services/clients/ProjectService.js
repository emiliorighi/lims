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
    return base.get(`/projects/${id}/statistics/${model}/${field}`)
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
  inferAttributesProject(data) {
    return base.post('/projects/wrangling', data)
  }
  inferHeadersFromTSV(projectId, data) {
    return base.post(`/projects/${projectId}/match_headers`, data)
  }
  uploadTSV(projectId, data) {
    return base.post(`/projects/${projectId}/upload`, data)
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
  updateDraftProject(id, data) {
    return base.put(`/draft_projects/${id}`, data)
  }
}

export default new ProjectService();
