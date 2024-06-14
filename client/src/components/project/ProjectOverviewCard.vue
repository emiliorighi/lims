<template>
    <va-card square outlined>
        <va-tree-view expand-all :nodes="nodes">
            <template #content="node">
                <div class="flex items-center">
                    <div class="mr-2">
                        <b v-if="node.key" class="display-6">{{ node.key }}</b>
                        <p v-if="node.label" class="va-text-secondary mb-0">
                            {{ node.label }}
                        </p>
                    </div>
                </div>
            </template>
        </va-tree-view>
    </va-card>
</template>
<script setup lang="ts">
import { TreeNode } from 'vuestic-ui/web-components';
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
</script>