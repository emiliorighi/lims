import http from "../../http";

const { base, yaml } = http

class StatsService {

    getStats(model, field) {
        return base.get(`/statistics/${model}/${field}`)
    }

}

export default new StatsService();
