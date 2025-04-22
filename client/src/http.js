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


function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

submitInstance.interceptors.request.use(
  (config) => {
      config.headers = {
          'X-CSRF-TOKEN': getCookie('csrf_access_token'),
          'Content-Type': 'application/json',
      }
      config.xsrfCookieName = 'csrf_access_token'
      config.xsrfHeaderName = 'X-CSRF-TOKEN'
      return config
  },
  (error) => {
      return Promise.reject(error)
  },
)


const download = axios.create({
  baseURL: baseURL, responseType: 'blob'
})

export default {
  submission: submitInstance,
  base: base,
  yaml: yaml,
  download: download
}
