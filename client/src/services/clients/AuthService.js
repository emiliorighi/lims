import http from '../../http'

const base = http.base

const auth = http.submission

function getCookie(name) {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop().split(';').shift()
}

auth.interceptors.request.use(
    (config) => {
        config.headers = {
            'X-CSRF-TOKEN': getCookie('csrf_access_token'),
            'Content-Type': 'application/json',
        }
        config.xsrfCookieName = 'csrf_access_token'
        config.xsrfHeaderName = 'X-CSRF-TOKEN'
        return config
    },
    (error) => {
        return Promise.reject(error)
    },
)


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
        return base.get('/users', { params: params })
    }
    getUser(id) {
        return auth.get(`/users/${id}`)
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
    deleteRecord(projectId, modelName, itemId) {
        return auth.delete(`/projects/${projectId}/models/${modelName}/records/${itemId}`)
    }
    createModel(projectId, data) {
        return auth.post(`/projects/${projectId}/models`, data)
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
    uploadTSV(projectId, data) {
        return auth.post(`/projects/${projectId}/upload`, data)
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
