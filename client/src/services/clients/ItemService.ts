import { ModelType } from "../../data/types";
import http from "../../http";
const { base, download } = http;

class ItemService {
    
    private constructUrl(projectId: string, model: ModelType, itemId?: string, suffix: string = ''): string {
        return itemId
            ? `/projects/${projectId}/${model}s/${itemId}${suffix}`
            : `/projects/${projectId}/${model}s${suffix}`;
    }

    getItems(projectId: string, model: ModelType, params: Record<string, any>) {
        return base.get(this.constructUrl(projectId, model), { params });
    }

    getItem(projectId: string, itemId: string, model: ModelType) {
        return base.get(this.constructUrl(projectId, model, itemId));
    }

    createItem(projectId: string, model: ModelType, data: FormData) {
        return base.post(this.constructUrl(projectId, model), data);
    }

    updateItem(projectId: string, itemId: string, model: ModelType, data: FormData) {
        return base.put(this.constructUrl(projectId, model, itemId), data);
    }

    deleteItem(projectId: string, itemId: string, model: ModelType) {
        return base.delete(this.constructUrl(projectId, model, itemId));
    }

    getTsv(projectId: string, model: ModelType, params: Record<string, any>) {
        return download.get(this.constructUrl(projectId, model), { params });
    }
    getStats(projectId:string,model:ModelType, field:string){
        return base.get(this.constructUrl(projectId, model, undefined, `/stats/${field}`))
    }
}

export default new ItemService();
