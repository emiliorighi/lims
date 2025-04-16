import http from "../../http";

const { base, download } = http;

class LinkService {

    getLinks(params) {
        return base.get('/links', { params });
    }
    getProjectModelLinks(projectId, modelName, params) {
        return base.get(`/projects/${projectId}/models/${modelName}/links`, { params });
    }
    uploadLinks(projectId, model, data){
        return base.post(`/projects/${projectId}/models/${model}/links`, data);
    }
    downloadLinks(hash){
        return download.get(`/files/${hash}/download`)
    }
}

export default new LinkService();
