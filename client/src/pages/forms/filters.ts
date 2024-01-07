import { ref } from 'vue'
import { Filter } from '../../data/types'

// by convention, composable function names start with "use"
export function useFilters(fields:Record<string,any>) {
  // state encapsulated and managed by the composable
  const filters = ref<Filter[]>([])

  filters.value = Object.keys(fields).map(f => {
    const filter:Filter = {
      label : fields[f].label?fields[f].label:f ,
      required: fields[f].required,
      value: '',
      type: fields[f].field_type,
      key: f
    }
    if(f.description)filter.description = f.description
    return filter
  })


  // expose managed state as return value
  return filters
}