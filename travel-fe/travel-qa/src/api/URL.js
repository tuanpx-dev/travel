export const URL = {
  // login
  LOGIN_EMAIL: '/auth/login_email/',
  LOGIN_FACEBOOK: '/auth/login_fb/',
  RESET_PASSWORD: '/auth/reset_password',

  // search
  SEARCH: `/questions/auth-required-search/`,

  // question
  QUESTIONS: (offset) => `/questions/auth-required-questions/?limit=10&offset=${offset}`,
  DETAIL_QUESTION: (id) => `/questions/auth-required-questions/${id}/`,
  DELETE_QUESTION: (id) => `/questions/${id}/`,
  EDIT_QUESTION: (id) => `/questions/${id}/`,
  CREATE_QUESTION: `/questions/`,
  LIKE_QUESTION: `/questions/likes/`,

  // category
  CATEGORY: '/category/',
  PROVINCE: '/area/provinces/',
  CITY: (provinceId) => `/area/citys/?province_id=${provinceId}`,
  AREA: (cityId) => `/area/areas/?city_id=${cityId}`,
  STATION: (cityId) => `/area/stations/?city_id=${cityId}`,

  // answers
  ANSWERS_QUESTION: (answerId) => `/questions/auth-required-questions/${answerId}/answers/`,
  CREATE_ANSWER: '/answers/',
  EDIT_ANSWER: (answerId) => `/answers/${answerId}/`,
  DELETE_ANSWER: (answerId) => `/answers/${answerId}/`,
  LIKE_ANSWER: `/answers/likes/`,

  // comment
  ANSWERS_COMMENT: (answerId) => `/answers/${answerId}/comments/`,
  CREATE_COMMENT: `comments/`,
  EDIT_COMMENT: (commentId) => `/comments/${commentId}/`,
  DELETE_COMMENT: (commentId) => `/comments/${commentId}/`,

  // profile
  EDIR_USER: `/user/profile/`,
  EDIT_PASS: `/user/change-password/`,
  MY_QUESTION: (offset) => `user/questions/?limit=10&offset=${offset}`,
  MY_ANSWER: (offset) => `user/answers/?limit=10&offset=${offset}`
}

export const URL_INCOGNITO = {
  // question
  QUESTIONS: (offset) => `/questions/?limit=10&offset=${offset}`,
  CREATE_QUESTION: `/questions/`,
  ANSWERS_QUESTION: (id) => `/questions/${id}/answers/`,
  DETAIL_QUESTION: (id) => `/questions/${id}/`,

  SEARCH: `/questions/search/`
}
