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
  createProject(data) {
    return base.post('/projects', data)
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
  uploadTSV(projectId, data) {
    return base.post(`/projects/${projectId}/upload_tsv`, data)
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
