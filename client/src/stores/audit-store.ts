import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AuditLog } from '../data/types'
import AuditService from '../services/clients/AuditService'

export const useAuditStore = defineStore('audit', () => {
  const auditLogs = ref<AuditLog[]>([])
  const totalLogs = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAuditLogs(params: {
    projectId?: string
    documentType?: string
    documentId?: string
    limit?: number
    offset?: number
    sortOrder?: string
  }) {
    loading.value = true
    error.value = null
    try {
      const { data } = await AuditService.getAuditLogs(params)
      auditLogs.value = data.data
      totalLogs.value = data.total
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch audit logs'
    } finally {
      loading.value = false
    }
  }

  async function fetchProjectAuditLogs(projectId: string, params: {
    limit?: number
    offset?: number
    sortOrder?: string
  }) {
    loading.value = true
    error.value = null
    try {
      const {data} = await AuditService.getProjectAuditLogs(projectId, params)
      auditLogs.value = data.data
      totalLogs.value = data.total
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch project audit logs'
    } finally {
      loading.value = false
    }
  }

  async function fetchDocumentAuditLogs(documentType: string, documentId: string, params: {
    limit?: number
    offset?: number
    sortOrder?: string
  }) {
    loading.value = true
    error.value = null
    try {
      const {data} = await AuditService.getDocumentAuditLogs(documentType, documentId, params)
      auditLogs.value = data.data
      totalLogs.value = data.total
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch document audit logs'
    } finally {
      loading.value = false
    }
  }

  return {
    auditLogs,
    totalLogs,
    loading,
    error,
    fetchAuditLogs,
    fetchProjectAuditLogs,
    fetchDocumentAuditLogs
  }
}) 