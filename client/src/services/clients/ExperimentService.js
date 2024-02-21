import http from "../../http";

const { base, auth } = http

class ExperimentService {

    getExperiments(projectId, params) {
        return base.get(`/projects/${projectId}/experiments`, { params: params })
    }
    getExperiment(projectId, experimentId) {
        return base.get(`/projects/${projectId}/experiments/${experimentId}`)
    }
    createExperiment(projectId, sampleId, data) {
        return base.post(`/projects/${projectId}/samples/${sampleId}/experiments`, data)
    }
    updateExperiment(projectId, sampleId, experimentId, data) {
        return base.put(`/projects/${projectId}/samples/${sampleId}/experiments/${experimentId}`, data)
    }
    deleteExperiment(projectId, sampleId, experimentId) {
        return base.delete(`/projects/${projectId}/samples/${sampleId}/experiments/${experimentId}`)
    }
}

export default new ExperimentService();
