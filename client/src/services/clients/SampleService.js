import http from "../../http";

const { base, auth } = http

class SampleService {

    getSamples(projectId, params) {
        return base.get(`/projects/${projectId}/samples`, { params: params })
    }
    getSample(projectId, sampleId) {
        return base.get(`/projects/${projectId}/samples/${sampleId}`)
    }
    createSample(projectId, data) {
        return base.post(`/projects/${projectId}/samples`, data)
    }
    updateSample(projectId, sampleId, data) {
        return base.put(`/projects/${projectId}/samples/${sampleId}`, data)
    }
    deleteSample(projectId, sampleId) {
        return base.delete(`/projects/${projectId}/samples/${sampleId}`)
    }
    uploadSampleTSV(projectId, data){
        return base.post(`/projects/${projectId}/samples/upload`, data)
    }
}

export default new SampleService();
