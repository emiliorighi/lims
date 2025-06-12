import http from "../../http";

const { base } = http;

class AuditService {
    getAuditLogs(params) {
        return base.get('/audit-logs', { params });
    }

    getProjectAuditLogs(projectId, params) {
        return base.get(`/projects/${projectId}/audit-logs`, { params });
    }

    getDocumentAuditLogs(documentType, documentId, params) {
        return base.get(`/audit-logs/${documentType}/${documentId}`, { params });
    }
}

export default new AuditService(); 