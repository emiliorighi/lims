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
        return auth.get('/login')
    }
    login(payload) {
        return base.post('/login', payload)
    }
    logout() {
        return base.get('/logout')
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
    createProject(data) {
        return auth.post('/projects', data)
    }
    createDraftProject(data) {
        return auth.post('/draft_projects', data)
    }
    updateDraftProject(id, data) {
        return auth.put(`/draft_projects/${id}`, data)
      }
    createItem(projectId, model, data) {
        return auth.post(`/projects/${projectId}/${model}s`, data)
    }
    updateItem(projectId, itemId, model, data) {
        return auth.put(`/projects/${projectId}/${model}s/${itemId}`, data)
    }
    deleteItem(projectId, itemId, model) {
        return auth.delete(`/projects/${projectId}/${model}s/${itemId}`)
    }
    uploadTSV(projectId, data) {
        return auth.post(`/projects/${projectId}/upload_tsv`, data)
    }
}

export default new AuthService()
