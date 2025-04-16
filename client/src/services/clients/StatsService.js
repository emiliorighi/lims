import http from "../../http";

const { base } = http

class StatsService {

    getStats(projectId, model, field, params) {
        return base.get(`/projects/${projectId}/models/${model}/stats/${field}`, { params });
    }
    lookupData() {
        return base.get('/lookup')
    }
    getModelStats(projectId, model) {
        return base.get(`/projects/${projectId}/models/${model}/lookup`);
    }
    getRecordStats(field, params) {
        return base.get(`/records/stats/${field}`, { params });
    }
    getLinkStats(field, params) {
        return base.get(`/links/stats/${field}`, { params })
    }
}

export default new StatsService();
