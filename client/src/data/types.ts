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
  [K in keyof T]?: T[K]
}


export type Filter = {
  label: string
  description?: string
  type: GeneralFilter<Input> | GeneralFilter<Select> | GeneralFilter<Range> | GeneralFilter<Boolean>
  key: string
  required: boolean
  value: string
}

export type Input = {
  type: 'string' | 'number' | 'date'
  regex: undefined | ''
}

export type Select = {
  type: 'select'
  multi: false
  choices: string[]
}

export type Range = {
  type: 'range'
  min: string
  max: string
  unit: string
}

export interface SearchForm {
  filter: string
  filter_option?: string
  sort_column: string
  sort_order: string
  start_date?: string
  end_date?: string
}