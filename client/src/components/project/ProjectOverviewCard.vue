<template>
    <VaTreeView expand-all :nodes="nodes">
        <template #content="node">
            <div class="flex items-center">
                <div class="mr-2">
                    <b v-if="node.key" class="display-6">{{ node.label === '$date' ? parseTimestamp(node.key) : node.key
                        }}</b>
                    <p v-if="node.label" class="va-text-secondary mb-0">
                        {{ node.label }}
                    </p>
                </div>
            </div>
        </template>
    </VaTreeView>
</template>
<script setup lang="ts">
import { TreeNode, VaTreeView } from 'vuestic-ui/web-components';
import { SchemaForm } from '../../data/types';

const props = defineProps<{
    metadata: SchemaForm
}>()

const nodes = buildTree(props.metadata, undefined)

function buildTree(data: SchemaForm, parentKey: string | undefined): TreeNode[] {
    const treeNodes: TreeNode[] = [];
    //
    Object.entries(data).filter(([k, v]) => Boolean(v)).forEach(([k, v]) => {
        const value = v
        const id = parentKey ? `${parentKey}-${k}` : k
        if (Array.isArray(value)) {
            // If the value is an array, create child nodes for each item in the array
            const childNodes = value.flatMap((item: any) => {
                if (typeof item === 'string') {
                    return { id: `${value}-${item}`, key: item, label: k };
                } else {
                    return buildTree(item, id);
                }
            });
            treeNodes.push({ id: id, label: k, children: childNodes });
        }
        else if (typeof value === 'object') {
            // If the value is an object, recursively build child nodes
            const childNodes = buildTree(value, id);
            treeNodes.push({ id: id, label: k, children: childNodes });
        } else {
            treeNodes.push({ id: id, label: k, key: value });

        }
    })
    return treeNodes;
}

function parseTimestamp(timestamp: number): string {
    // Create a Date object from the timestamp
    const date = new Date(timestamp);

    // Extract date components
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    // Format the date as "YYYY-MM-DD HH:MM:SS"
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

</script>