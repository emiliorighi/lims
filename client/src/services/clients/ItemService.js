import http from "../../http";

const { base, download } = http;

class ItemService {

    getItems(projectId, model, params) {
        return base.get(`/projects/${projectId}/${model}s`, { params });
    }
    getItem(projectId, itemId, model) {
        return base.get(`/projects/${projectId}/${model}s/${itemId}`);
    }
    getTsv(projectId, model, params) {
        return download.get(`/projects/${projectId}/${model}s`, { params });
    }
    getStats(projectId, model, field) {
        return base.get(`/projects/${projectId}/${model}s/stats/${field}`)
    }
}

export default new ItemService();
