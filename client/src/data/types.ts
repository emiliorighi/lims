import type { TChartData as ChartData } from 'vue-chartjs/dist/types'

export type ColorThemes = {
  [key: string]: string
}

export type InputType = 'text' | 'date' | 'number' | 'select'
export type ChartTypes = "line" | "bar" | "bubble" | "doughnut" | "pie" | "horizontal-bar"
export type ModelKeys = 'projects' | 'models' | 'protocols' | 'records' | 'images'
export type LinkType = 'images'|'protocols'|'analysis'
export type ChartItem = {
  type: ChartTypes
  data: any
  label: string
  chartId: string
  chartOptions: any
}
export type QueryFilter = {
  key: string
  option?: 'single' | 'range'
  type: InputType
  query: Record<string, any>
}

export type ProtocolForm = {
  name: string,
  description: string,
  files: File[],
}
export type TLineChartData = ChartData<'line'>
export type TBarChartData = ChartData<'bar'>
export type TBubbleChartData = ChartData<'bubble'>
export type TDoughnutChartData = ChartData<'doughnut'>
export type TPieChartData = ChartData<'pie'>
export interface ErrorResponseData {
  message?: string; // Optional, because not all error responses may contain a message
}
export type TChartData = TLineChartData | TBarChartData | TBubbleChartData | TDoughnutChartData | TPieChartData

export type FieldType = "input" | "select" | "range";

export type Theme = "light" | "dark"
export type UserRole = 'admin' | 'project_manager'

export type ItemModel = {
  experiment_id?: string,
  sample_id: string,
  metadata: Record<string, any>
}


//PROJECT TO CREATE SCHEMA
export type ProjectSchema = {
  project_id: string,
  name: string,
  version: string,
  description?: string,
  models: ResearchModel[],
  drafted?: boolean,
  archived?: boolean
}

export type ResearchRecord = {
  item_id: string;
  reference_id?: string;
  project_id: string,
  model_name: string,
  created: {
    $date: Date
  },
  [key: string]: unknown; // Allows additional properties
}

//MODEL 
export type ModelSchema = {
  name: string,
  description: string,
  reference_model?: string,
  protocols: { name: string, description?: string, file: any }[],
  links: { name: string, link: string, description?: string }[]
  fields: ResearchFilter[],
  id_format: string[]
}

export type Projectd = {
  project_id: string,
  name: string,
  version: string,
  description?: string,
  models: string[]
  drafted?: boolean,
  archived?: boolean
}

export type ModelType = {

}
export type User = {
  name: string,
  password?: string
  projects: string[]
  role: UserRole
}
export const fieldTypes = ['input', 'select', 'range']

export type Input = {
  input_type: 'text' | 'number' | 'date'
  regex?: string
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
export type Project = {
  project_id: string,
  name: string,
  version: string,
  description?: string,
  models: string[]
  drafted?: boolean,
  archived?: boolean
}

export interface ReseachProject {
  project_id: string,
  name: string,
  version: string,
  description?: string,
  models: ResearchModel[]
  drafted?: boolean,
  archived?: boolean
}

export type ResearchModel = {
  name: string,
  description: string,
  reference_model?: string,
  project_id?: string,
  fields: ResearchFilter[],
  id_format: string[]

}

export type FileModelLink = {
  name: string,
  description?: string,
  hash: string,
  extension: string

}

export type ResearchFilter = {
  description?: string
  type: 'text' | 'date' | 'number' | 'select'
  multi?: boolean
  choices?: string[]
  regex?: string
  key: string
  required: boolean
  value?: string
  model?: ModelType
  fromTSV?: boolean,
  tsvKey?: string
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

export type VaChartItem = {
  type: ChartTypes
  data: Record<string, number>
  model: 'sample' | 'experiment',
  field: string
  size: ColumnSizes
}

export type ColumnSizes = '1' | '2' | '3' | '4'