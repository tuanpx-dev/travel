export const URL = {
  // login
  LOGIN_EMAIL: '/auth/login_email/',
  LOGIN_FACEBOOK: '/auth/login_fb/',
  RESET_PASSWORD: '/auth/reset_password',

  // question
  QUESTIONS: (offset) => `/questions/auth-required-questions/?limit=10&offset=${offset}`,
  ANSWERS_QUESTION: (id) => `/questions/auth-required-questions/${id}/answers/`,
  DETAIL_QUESTION: (id) => `/questions/auth-required-questions/${id}/`,
  DELETE_QUESTION: (id) => `/questions/${id}/`,
  CREATE_QUESTION: `/questions/`,
  LIKE_QUESTION: `/questions/likes/`,

  // category
  CATEGORY: '/category/',

  // answers
  ANSWERS: '/answers/'
}

export const URL_INCOGNITO = {
  // question
  QUESTIONS: (offset) => `/questions/?offset=${offset}`,
  CREATE_QUESTION: `/questions/`,
  ANSWERS_QUESTION: (id) => `/questions/${id}/answers/`,
  DETAIL_QUESTION: (id) => `/questions/${id}/`
}
