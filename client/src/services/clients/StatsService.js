import http from "../../http";

const { base } = http

class StatsService {

    getStats(projectId, model, field, params) {
        return base.get(`/projects/${projectId}/models/${model}/stats/${field}`, { params });
    }
    lookupData() {
        return base.get('/lookup')
    }

}

export default new StatsService();
