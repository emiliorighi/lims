<template>
  <div>
    <div class="row align-end justify-space-between">
      <div class="flex">
        <h1 class="va-h1">Audit Logs</h1>
        <p class="va-text-secondary">
          Track changes across the system
        </p>
      </div>
    </div>
    <div class="row">
      <div class="flex lg12 md12 sm12 xs12">
        <VaCard>
          <VaCardContent>
            <div class="row align-center justify-space-between">
              <div class="flex">
                <div class="row">
                  <div class="flex">
                    <VaSelect
                      v-model="searchForm.document_type"
                      :options="documentTypeOptions"
                      placeholder="Document Type"
                      clearable
                    />
                  </div>
                  <div class="flex">
                    <VaInput
                      v-model="searchForm.document_id"
                      placeholder="Search by Document ID"
                      clearable
                    />
                  </div>
                  <div class="flex">
                    <VaSelect
                      :options="projects"
                      v-model="searchForm.project_id"
                      placeholder="Search by Project ID"
                      clearable
                    />
                  </div>
                  <div class="flex">
                    <VaSelect
                      :options="users"
                      v-model="searchForm.user"
                      placeholder="Search by User"
                      clearable
                    />
                  </div>
                </div>
              </div>
            </div>
            <VaDataTable
              :items="auditStore.auditLogs"
              :columns="columns"
              :loading="auditStore.loading"
            >
              <!-- Action Column -->
              <template #cell(action)="{ value }">
                <VaChip size="small" :color="getActionColor(value)">
                  {{ value }}
                </VaChip>
              </template>
              <!-- Project ID Column -->
              <template #cell(project_id)="{ value }">
                <VaChip size="small" color="backgroundElement">
                  {{ value }}
                </VaChip>
              </template>
              <!-- Document Type Column -->
              <template #cell(document_type)="{ value }">
                <VaChip size="small" color="info">
                  {{ value }}
                </VaChip>
              </template>

              <!-- Changes Column -->
              <template #cell(changes)="{ rowData }">
                <VaButton
                  size="small"
                  @click="showChanges(rowData)"
                >
                  View Changes
                </VaButton>
              </template>

              <!-- Created Column -->
              <template #cell(timestamp.$date)="{ value }">
                {{ formatDate(value) }}
              </template>
            </VaDataTable>
          </VaCardContent>
          <VaCardContent>
            <div class="row justify-space-between align-center">
              <div class="flex">
                Results: {{ auditStore.totalLogs }}
              </div>
              <div class="flex">
                <div class="row justify-center">
                  <div class="flex">
                    <VaPagination
                      v-model="offset"
                      :page-size="limit"
                      :total="auditStore.totalLogs"
                      :visible-pages="3"
                      buttons-preset="primary"
                      gapped
                    />
                  </div>
                </div>
              </div>
            </div>
          </VaCardContent>
        </VaCard>
      </div>
    </div>

    <!-- Changes Modal -->
    <VaModal
      v-model="showChangesModal"
      title="Changes"
      :message="''"
    >
      <AuditDiff
        :previous="selectedChanges.previous_object"
        :current="selectedChanges.new_object"
      />
    </VaModal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, watch, onMounted } from 'vue'
import { useAuditStore } from '../stores/audit-store'
import AuditDiff from '../components/AuditDiff.vue'
import AuthService from '../services/clients/AuthService'
import ProjectService from '../services/clients/ProjectService'

const auditStore = useAuditStore()
const limit = 10
const showChangesModal = ref(false)
const selectedChanges = ref<{ previous_object: Record<string, any> | null; new_object: Record<string, any> | null }>({previous_object: null, new_object: null})

const users = ref<string[]>([])
const projects = ref<string[]>([])
const searchForm = reactive({
  document_type: null as string | null,
  document_id: '',
  project_id: '',
  user: '',
})

const pagination = reactive({
  offset: 0,
  limit: 10,
})

const offset = computed({
  get() {
    return pagination.offset + 1
  },
  set(v: number) {
    pagination.offset = v - 1
  }
})

const documentTypeOptions = ['project', 'model', 'record', 'file_link']

const columns = [
  { key: 'timestamp.$date', label: 'Date' },
  { key: 'user', label: 'User' },
  { key: 'action', label: 'Action' },
  { key: 'document_type', label: 'Document Type' },
  { key: 'document_id', label: 'Document ID' },
  { key: 'project_id', label: 'Project ID' },
  { key: 'changes', label: 'Changes' }
]

function getActionColor(action: string): string {
  const colors: Record<string, string> = {
    create: 'success',
    update: 'warning',
    delete: 'danger',
    archive: 'info',
    unarchive: 'info',
    clone: 'primary',
    upload: 'success',
    download: 'info'
  }
  return colors[action] || 'primary'
}

function formatDate(date: string): string {
  return new Date(date).toLocaleString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).split(',')[0].replace(/(\d+)\/(\d+)\/(\d+)/, '$3-$1-$2')
}

function showChanges(changes: Record<string, any>) {
  selectedChanges.value = {
    previous_object: Object.keys(changes.previous_object).length > 0 ? changes.previous_object : null,
    new_object: Object.keys(changes.new_object).length > 0 ? changes.new_object : null
  }
  showChangesModal.value = true
}

watch(() => searchForm, async () => {
  const params = {
    document_type: searchForm.document_type || undefined,
    document_id: searchForm.document_id || undefined,
    project_id: searchForm.project_id || undefined,
    user: searchForm.user || undefined
  }
  pagination.offset = 0
  await auditStore.fetchAuditLogs({...params, ...pagination})
}, { immediate: true, deep: true })

watch(() => offset.value, async () => {
  const params = {
    document_type: searchForm.document_type || undefined,
    document_id: searchForm.document_id || undefined,
    project_id: searchForm.project_id || undefined,
    user: searchForm.user || undefined
  }
  await auditStore.fetchAuditLogs({...params, ...pagination})
})


async function getUsers() {
  const {data} = await AuthService.getUsers({limit: 10000})
  users.value = data.data.map((user: any) => user.name)
}
async function getProjects() {
  const {data} = await ProjectService.getProjects({limit: 10000})
  projects.value = data.data.map((project: any) => project.project_id)
}

onMounted(async () => {
  await getUsers()
  await getProjects()
})

</script>

<style scoped>
.va-h1 {
  margin-bottom: 0.5rem;
}
</style> 