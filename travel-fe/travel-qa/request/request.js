import axios from 'axios'
let user = JSON.parse(localStorage.getItem('user'))

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
    config.headers['Authorization'] = 'Bearer '
    if (user) {
      config.headers['Authorization'] = 'Bearer ' + user.data.access_token
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
