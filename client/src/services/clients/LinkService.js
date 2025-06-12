import http from "../../http";

const { base, download, submission } = http;

class LinkService {

    getLinks(params) {
        return base.get('/links', { params });
    }
    getProjectModelLinks(projectId, modelName, params) {
        return base.get(`/projects/${projectId}/models/${modelName}/links`, { params });
    }
    downloadLinks(hash){
        return download.get(`/files/${hash}/download`)
    }
    downloadFiles(projectId, modelName, type) {
        return download.get(`/projects/${projectId}/models/${modelName}/files/${type}/download`)
    }
    uploadLinks(projectId, model, data) {
        return submission.post(`/projects/${projectId}/models/${model}/links`, data);
    }
    deleteLink(projectId, model, name, type) {
        return submission.delete(`/projects/${projectId}/models/${model}/links/${type}/${name}`);
    }
}

export default new LinkService();
