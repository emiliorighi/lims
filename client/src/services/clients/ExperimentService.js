import http from "../../http";

const { base, download } = http

class ExperimentService {

    getExperiments(projectId, params) {
        return base.get(`/projects/${projectId}/experiments`, { params: params })
    }
    getExperiment(projectId, experimentId) {
        return base.get(`/projects/${projectId}/experiments/${experimentId}`)
    }
    createExperiment(projectId, data) {
        return base.post(`/projects/${projectId}/experiments`, data)
    }
    updateExperiment(projectId, experimentId, data) {
        return base.put(`/projects/${projectId}/experiments/${experimentId}`, data)
    }
    deleteExperiment(projectId, experimentId) {
        return base.delete(`/projects/${projectId}/experiments/${experimentId}`)
    }
    uploadExperimentTSV(projectId, data) {
        return base.post(`/projects/${projectId}/experiments/upload`, data)
    }
    getTsv(projectId, params) {
        return download.get(`/projects/${projectId}/experiments`, { params: params })
    }
    getAllExperiments(params){
        return base.get('/experiments', {params:params})
    }
}

export default new ExperimentService();
