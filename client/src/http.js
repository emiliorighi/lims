import axios from 'axios'

const baseURL = import.meta.env.VITE_API_PATH ?
  import.meta.env.VITE_API_PATH : import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL + 'api' : import.meta.env.BASE_URL + '/api'

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
  baseURL: baseURL, responseType: 'blob'
})

export default {
  submission: submitInstance,
  base: base,
  yaml: yaml,
  download: download
}
