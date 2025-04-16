<template>
  <div ref="chartDiv" style="width: 100%; height: 400px;"></div>
</template>
<script lang="ts" setup>
import * as am5 from "@amcharts/amcharts5";
import * as am5hierarchy from "@amcharts/amcharts5/hierarchy";
import * as am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
import { onBeforeUnmount, onMounted, ref, shallowRef, watch } from "vue";


const chartDiv = ref<HTMLDivElement | null>(null);
const root = shallowRef<am5.Root | null>(null);

const props = defineProps<{
  roots: any[]
}>()

// Cleanup function
function disposeChart() {
  if (root.value) {
    root.value.dispose();
    root.value = null;
  }
}

// React to changes in mappedModels
watch(() => props.roots, () => {
  // Dispose existing chart if needed
  disposeChart()
  const treeData = {
    name: 'Models Relationship',
    children: props.roots
  }
  createChart(treeData);
});


onMounted(() => {
  const treeData = {
    name: 'Models Relationship',
    children: props.roots
  }
  createChart(treeData);
})

// Dispose chart on unmount
onBeforeUnmount(() => {
  disposeChart();
});

// Create chart instance
function createChart(data: any) {
  if (!chartDiv.value) return

  root.value = am5.Root.new(chartDiv.value);
  root.value.setThemes([am5themes_Animated.default.new(root.value)]);

  const series = root.value.container.children.push(
    am5hierarchy.ForceDirected.new(root.value, {
      singleBranchOnly: false,
      downDepth: 1,
      topDepth: 1,
      initialDepth: 2,
      valueField: "value",
      categoryField: "name",
      childDataField: "children",
      idField: "name",
      linkWithField: "linkWith",
      minRadius: 30,
      maxRadius: am5.percent(20),
    })
  )

  series.data.setAll([data]);
  series.set("selectedDataItem", series.dataItems[0]);
}

</script>
<style scoped></style>
