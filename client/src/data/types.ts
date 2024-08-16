import type { TChartData as ChartData } from 'vue-chartjs/dist/types'

export type ColorThemes = {
  [key: string]: string
}

export type TLineChartData = ChartData<'line'>
export type TBarChartData = ChartData<'bar'>
export type TBubbleChartData = ChartData<'bubble'>
export type TDoughnutChartData = ChartData<'doughnut'>
export type TPieChartData = ChartData<'pie'>

export type TChartData = TLineChartData | TBarChartData | TBubbleChartData | TDoughnutChartData | TPieChartData

export type FieldType = "input" | "select" | "range";

export type Theme = "light" | "dark"
export type ModelType = "sample" | "experiment"

export type ItemModel = {
  experiment_id?: string,
  sample_id: string,
  metadata: Record<string, any>
}

export const fieldTypes = ['input', 'select', 'range']

export type Input = {
  input_type: 'text' | 'number' | 'date'
  regex: undefined | ''
}

export type Select = {
  multi: false
  choices: string[]
}

export type Range = {
  min: number
  max: number
  unit: string
}
export interface ModelSearchForm {
  filter: string
  query: Record<string, any>
  sort_column: string,
  sort_order: 'asc' | 'desc'
}
export interface SchemaForm {
  project_id: string,
  name: string,
  version: string,
  description?: string,
  sample: ProjectModel,
  experiment: ProjectModel,
  created?: { $date: number }
}

export type ProjectModel = {
  fields: Filter[],
  id_format: string[]
}

export type Filter = {
  label: string
  description?: string
  filter: Input | Select | Range
  key: string
  required: boolean
  value?: string
  model?: ModelType
}

export interface SearchForm {
  filter: string
  filter_option?: string
  sort_column: string
  sort_order: string
  start_date?: string
  end_date?: string
}

export type DashboardCard = {
  icon: string,
  text: string,
  color: string,
  count: number | null
}

export type ChartTypes = "line" | "bar" | "doughnut" | "pie" | "horizontal-bar"
export type VaChartItem = {
  type: ChartTypes
  data: Record<string, number>
  model: 'sample' | 'experiment',
  field: string
  size: ColumnSizes
}

export type ColumnSizes = '1' | '2' | '3' | '4'