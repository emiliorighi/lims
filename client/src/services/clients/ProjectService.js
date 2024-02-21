import http from "../../http";

const { base, auth } = http

class ProjectService {

  getProjects(params) {
    return base.get('/projects', { params: params })
  }
  getProject(id) {
    return base.get(`/projects/${id}`)
  }
  createProject(data) {
    return base.post('/projects', data)
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
