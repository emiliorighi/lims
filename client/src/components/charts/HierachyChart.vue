<template>
  <div class="chart-wrapper">
    <div ref="chartDiv" class="chart-container"></div>
  </div>
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

  const container = root.value.container.children.push(
    am5.Container.new(root.value, {
      width: am5.percent(100),
      height: am5.percent(100),
      paddingRight: 15,
      paddingLeft: 15,
      layout: root.value.verticalLayout
    })
  )
  const series = container.children.push(
    am5hierarchy.Tree.new(root.value, {
      singleBranchOnly: false,
      downDepth: 1,
      topDepth: 1,
      initialDepth: 10,
      valueField: "value",
      categoryField: "name",
      childDataField: "children",
      idField: "name",
      orientation: "vertical"
    })
  )
  series.circles.template.setAll({
    radius: 40
  });

  series.outerCircles.template.setAll({
    radius: 40
  });

  series.data.setAll([data]);
  series.set("selectedDataItem", series.dataItems[0]);
}

</script>
<style scoped>
.chart-container {
  width: 100%;
  min-height: 400px;
}
</style>