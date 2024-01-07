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
    login(payload) {
        return base.post('/login', payload)
    }
    logout() {
        return base.get('/logout')
    }
    createExperiment(payload){
        return auth.post('/experiments', payload)
    }
    updateExperiment(id, payload){
        return auth.put(`/experiments/${id}`, payload)
    }
    deleteExperiment(id){
        return auth.delete(`/experiments/${id}`)
    }
    createSample(payload){
        return auth.post('/samples', payload)
    }
    updateSample(id, payload){
        return auth.put(`/samples/${id}`, payload)
    }
    deleteSample(id){
        return auth.delete(`/samples/${id}`)
    }}
export default new AuthService()
