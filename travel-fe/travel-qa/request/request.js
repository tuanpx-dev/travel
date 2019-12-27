import axios from 'axios'

// create an axios instance
const service = axios.create({
  baseURL: 'http://34.87.111.216:8000',
  timeout: 0,
  headers: {
    'Content-Type': 'application/json'
  }
})

// request interceptor
service.interceptors.request.use(
  config => {
    let token = JSON.parse(localStorage.getItem('user'))

    if (token) {
      config.headers['Authorization'] = `Bearer ${token.data.access_token}`
    }

    return config
  },
  error => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  response => response,
  error => {
    return Promise.reject(error)
  }
)

export default service
