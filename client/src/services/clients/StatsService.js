import http from "../../http";

const { base } = http

class StatsService {

    getStats(model, field) {
        return base.get(`/${model}/stats/${field}`)
    }
    lookupData() {
        return base.get('/lookup')
    }

}

export default new StatsService();
