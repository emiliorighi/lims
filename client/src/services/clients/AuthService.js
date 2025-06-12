import http from '../../http'

const base = http.base

const auth = http.submission

class AuthService {
    check() {
        return auth.get('/auth/login')
    }
    login(payload) {
        return base.post('/auth/login', payload)
    }
    logout() {
        return base.get('/auth/logout')
    }
    getUsers(params) {
        return auth.get('/users', { params: params })
    }
    getUser(id) {
        return auth.get(`/users/${id}`)
    }
    archiveProject(id) {
        return auth.patch(`/projects/${id}/archive`)
    }
    unarchiveProject(id) {
        return auth.patch(`/projects/${id}/unarchive`)
    }
    createUser(payload) {
        return auth.post('/users', payload)
    }
    updateUser(id, payload) {
        return auth.put(`/users/${id}`, payload)
    }
    deleteUser(id) {
        return auth.delete(`/users/${id}`)
    }
    createResearchProject(data) {
        return auth.post('/projects', data)
    }
    createRecord(projectId, modelName, data) {
        return auth.post(`/projects/${projectId}/models/${modelName}/records`, data)
    }
    updateRecord(projectId, modelName, itemId, data) {
        return auth.put(`/projects/${projectId}/models/${modelName}/records/${itemId}`, data)
    }
    deleteRecords(projectId, modelName) {
        return auth.delete(`/projects/${projectId}/models/${modelName}/records`)
    }
    deleteRecord(projectId, modelName, itemId) {
        return auth.delete(`/projects/${projectId}/models/${modelName}/records/${itemId}`)
    }
    createModel(projectId, data) {
        return auth.post(`/projects/${projectId}/models`, data)
    }
    updateModel(projectId, modelName, data) {
        return auth.put(`/projects/${projectId}/models/${modelName}`, data)
    }
    deleteModel(projectId, modelName) {
        return auth.delete(`/projects/${projectId}/models/${modelName}`)
    }
    createItem(projectId, model, data) {
        return auth.post(`/projects/${projectId}/${model}s`, data)
    }
    updateItem(projectId, itemId, model, data) {
        return auth.put(`/projects/${projectId}/${model}s/${itemId}`, data)
    }
    deleteItem(projectId, itemId, model) {
        return auth.delete(`/projects/${projectId}/models/${model}/${itemId}`)
    }
    uploadTSV(projectId, modelName, data) {
        return auth.post(`/projects/${projectId}/models/${modelName}/records/upload`, data)
    }
    uploadProtocol(projectId, model, data) {
        return auth.post(`/projects/${projectId}/models/${model}/protocols`, data);
    }
    deleteProtocol(projectId, model, name) {
        return auth.delete(`/projects/${projectId}/models/${model}/protocols/${name}`);
    }
    uploadLinks(projectId, model, data) {
        return auth.post(`/projects/${projectId}/models/${model}/links`, data);
    }
    deleteLink(projectId, model, name, type) {
        return auth.delete(`/projects/${projectId}/models/${model}/links/${type}/${name}`);
    }
}

export default new AuthService()
