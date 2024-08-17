import axios from 'axios'

const baseURL = import.meta.env.VITE_BASE_PATH  ?  import.meta.env.VITE_BASE_PATH + '/api' : '/api' 

const base = axios.create({
  baseURL: baseURL,
  timeout: 60000,
  headers: {
    'Content-type': 'application/json',
  },
})

const yaml = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-type': 'application/x-yaml',
  }
})
const submitInstance = axios.create({
  baseURL: baseURL,
  timeout: 60000,
  headers: {
    'Content-type': 'application/json',
  },
})


const download = axios.create({
  baseURL: baseURL,
  timeout: 60000,
  responseType: 'blob'
})

export default {
  submission: submitInstance,
  base: base,
  yaml: yaml,
  download:download
}
