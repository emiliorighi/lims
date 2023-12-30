<template>
    <va-form tag="form" @submit.prevent="onSubmit">
      <va-card-content>
        <div class="row align-end">
          <div v-for="(filter, index) in filters" :key="index" class="flex lg3 md4 sm12 xs12">
            <div v-if="filter.field.name === 'input'">
              <va-input v-model="searchForm[filter.key]" :label="filter.label" />
            </div>
            <div v-else-if="filter.field.name === 'select'">
              <va-select v-model="searchForm[filter.key]" :label="filter.label" :options="filter.field.type.choices" searchable />
            </div>
            <!-- <div v-else-if="filter.type === 'date'">
              <va-date-input v-model="dateRange" :format-date="(date: Date) => date.toISOString().substring(0, 10)"
                :label="t(filter.label)" style="width: 100%" mode="range" type="month" prevent-overflow
                :allowed-years="(date: Date) => date <= new Date()" />
            </div>
            <div v-else-if="filter.type === 'checkbox'">
              <va-switch v-model="searchForm[filter.key]" :label="t(filter.label)" color="#9c528b" />
            </div> -->
          </div>
          <div class="flex"> <va-button :disabled="!validFilters" type="submit">Submit</va-button>
          </div>
          <div class="flex"> <va-button color="danger" @click="onReset">Reset</va-button>
          </div>
        </div>
      </va-card-content>
    </va-form>
  </template>
  <script setup lang="ts">
  import { computed } from 'vue'
  import { Filter } from '../../data/types'
  
  
  const props = defineProps<{ filters: Array<Filter>, searchForm: Record<string, any> }>()
 
  
  const validFilters = computed(() => {
    const requiredFields = props.filters.filter(f => f.required).length
    const filledFields =  props.filters.filter(f => f.required && f.value ).length
    return requiredFields === filledFields
  })

  const emits = defineEmits(['onSubmit', 'onReset'])
  
  function onSubmit() {
    emits('onSubmit')
  }
  
  function onReset() {
    emits('onReset')
  }


</script>