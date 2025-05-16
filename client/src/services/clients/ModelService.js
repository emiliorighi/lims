import http from "../../http";

const { base } = http

class ModelService {
    getRelatedModelsRecordCount(projectId, modelName) {
        return base.get(`/projects/${projectId}/models/${modelName}/related_models_count`)
    }
}

export default new ModelService();
