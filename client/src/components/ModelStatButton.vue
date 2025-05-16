<template>
  <VaButton
    :to="{ 
      name: routeName,
      params: { 
        modelName: modelName,
        projectId: projectId 
      } 
    }"
    class="pa-0 ml-1"
    color="textPrimary"
    preset="plain"
  >
    <Counter :duration="1000" :target-value="value" />
  </VaButton>
</template>

<script>
import Counter from './ui/Counter.vue'

export default {
  name: 'ModelStatButton',
  components: {
    Counter
  },
  props: {
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