<template>
  <div class="flex mr-4">
    <p class="va-text-secondary">{{ label }}:</p>
    <ModelStatButton
      :route-name="routeName"
      :model-name="modelName"
      :project-id="projectId"
      :value="value"
    />
  </div>
</template>

<script>
import ModelStatButton from './ModelStatButton.vue'

export default {
  name: 'ModelStatItem',
  components: {
    ModelStatButton
  },
  props: {
    label: {
      type: String,
      required: true
    },
    routeName: {
      type: String,
      required: true
    },
    modelName: {
      type: String,
      required: true
    },
    projectId: {
      type: String,
      required: true
    },
    value: {
      type: Number,
      default: 0
    }
  }
}
</script> 