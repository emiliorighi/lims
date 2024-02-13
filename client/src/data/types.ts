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

type GeneralFilter<T> = {
  [K in keyof T]: T[K]
}
export type FieldType = "input" | "select" | "range";
export type ProjectModel = {
  fields : Filter[],
  id_format: string[]
}
export type SampleModel = {
  sample_id:string,
  metadata:Record<string,any>
}

export type ExperimentModel = {
  experiment_id:string,
  metadata:Record<string,any>
}
export const fieldTypes = ['input','select','range']

export type Filter = {
  label: string
  description?: string
  filter: Input | Select | Range
  key: string
  required: boolean
  value?: string
}

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
export interface SchemaForm {
  project_id: string,
  name: string,
  version: string,
  description?: string,
  sample: ProjectModel
  experiment: ProjectModel
}
export interface SearchForm {
  filter: string
  filter_option?: string
  sort_column: string
  sort_order: string
  start_date?: string
  end_date?: string
}