<template>
    <div class="audit-diff">
        <div v-if="!previous && !current" class="text-center">
            <p class="va-text-secondary">No changes to display</p>
        </div>
        <div v-else class="diff-container">
            <div v-for="(value, key) in diff" :key="key" class="diff-row">
                <div class="diff-key">{{ key }}</div>
                <div class="diff-value">
                    <div v-if="value.type === 'added'" class="diff-added">
                        <span class="diff-label">Added:</span>
                        <pre>{{ formatValue(value.value) }}</pre>
                    </div>
                    <div v-else-if="value.type === 'removed'" class="diff-removed">
                        <span class="diff-label">Removed:</span>
                        <pre>{{ formatValue(value.value) }}</pre>
                    </div>
                    <div v-else-if="value.type === 'modified'" class="diff-modified">
                        <div class="diff-old">
                            <span class="diff-label">Old:</span>
                            <pre>{{ formatValue(value.oldValue) }}</pre>
                        </div>
                        <div class="diff-new">
                            <span class="diff-label">New:</span>
                            <pre>{{ formatValue(value.newValue) }}</pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface DiffValue {
    type: 'added' | 'removed' | 'modified' | 'unchanged'
    value?: any
    oldValue?: any
    newValue?: any
}

const props = defineProps<{
    previous: Record<string, any> | null
    current: Record<string, any> | null
}>()

function formatValue(value: any): string {
    if (value === null || value === undefined) return 'null'
    if (typeof value === 'object') return JSON.stringify(value, null, 2)
    return String(value)
}

function compareValues(oldVal: any, newVal: any): DiffValue {
    if (oldVal === undefined && newVal !== undefined) {
        return { type: 'added', value: newVal }
    }
    if (oldVal !== undefined && newVal === undefined) {
        return { type: 'removed', value: oldVal }
    }
    if (JSON.stringify(oldVal) !== JSON.stringify(newVal)) {
        return { type: 'modified', oldValue: oldVal, newValue: newVal }
    }
    return { type: 'unchanged', value: oldVal }
}

const diff = computed(() => {
    const result: Record<string, DiffValue> = {}
    const allKeys = new Set([
        ...Object.keys(props.previous || {}),
        ...Object.keys(props.current || {})
    ])

    allKeys.forEach(key => {
        const oldVal = props.previous?.[key]
        const newVal = props.current?.[key]
        const diffValue = compareValues(oldVal, newVal)
        if (diffValue.type !== 'unchanged') {
            result[key] = diffValue
        }
    })

    return result
})
</script>

<style scoped>
.audit-diff {
    max-height: 70vh;
    overflow-y: auto;
    padding: 1rem;
}

.diff-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.diff-row {
    display: flex;
    gap: 1rem;
    padding: 0.5rem;
    border-radius: 4px;
    background-color: var(--va-background-primary);
}

.diff-key {
    min-width: 150px;
    font-weight: bold;
    color: var(--va-text-primary);
}

.diff-value {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.diff-added {
    color: var(--va-success);
}

.diff-removed {
    color: var(--va-danger);
}

.diff-modified {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.diff-old {
    color: var(--va-danger);
}

.diff-new {
    color: var(--va-success);
}

.diff-label {
    font-weight: bold;
    margin-right: 0.5rem;
}

pre {
    margin: 0;
    white-space: pre-wrap;
    word-break: break-word;
    background-color: var(--va-background-secondary);
    padding: 0.5rem;
    border-radius: 4px;
}
</style> 