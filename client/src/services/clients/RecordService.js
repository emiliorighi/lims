import http from "../../http";

const { base, download } = http;

class RecordService {

    getItems(projectId, model, params) {
        return base.get(`/projects/${projectId}/models/${model}/records`, { params });
    }
    getItem(projectId, itemId, model) {
        return base.get(`/projects/${projectId}/models/${model}/records/${itemId}`);
    }
    getTsv(projectId, model, params) {
        return download.get(`/projects/${projectId}/models/${model}/records`, { params });
    }
    getStats(projectId, model, field) {
        return base.get(`/projects/${projectId}/${model}s/stats/${field}`)
    }
    getRelatedRecords(projectId, modelName, itemId, params) {
        return base.get(`/projects/${projectId}/models/${modelName}/records/${itemId}/related_records`, { params });
    }
}

export default new RecordService();
