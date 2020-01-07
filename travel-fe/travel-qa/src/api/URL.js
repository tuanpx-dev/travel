export const URL = {
  // login
  LOGIN_EMAIL: '/auth/login_email/',
  LOGIN_FACEBOOK: '/auth/login_fb/',
  RESET_PASSWORD: '/auth/reset_password',

  // question
  QUESTIONS: (offset) => `/questions/auth-required-questions/?limit=10&offset=${offset}`,
  DETAIL_QUESTION: (id) => `/questions/auth-required-questions/${id}/`,
  DELETE_QUESTION: (id) => `/questions/${id}/`,
  CREATE_QUESTION: `/questions/`,
  LIKE_QUESTION: `/questions/likes/`,

  // category
  CATEGORY: '/category/',

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
  DELETE_COMMENT: (commentId) => `/comments/${commentId}/`
}

export const URL_INCOGNITO = {
  // question
  QUESTIONS: (offset) => `/questions/?offset=${offset}`,
  CREATE_QUESTION: `/questions/`,
  ANSWERS_QUESTION: (id) => `/questions/${id}/answers/`,
  DETAIL_QUESTION: (id) => `/questions/${id}/`
}
