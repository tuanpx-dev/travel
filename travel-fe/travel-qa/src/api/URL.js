export const URL = {
  // login
  LOGIN_EMAIL: '/auth/login_email/',
  LOGIN_FACEBOOK: '/auth/login_fb/',

  // question
  QUESTIONS: '/questions/',
  LIKE_QUESTION: `/questions/like/`,
  ANSWERS_QUESTION: (id) => `/questions/${id}/answers/`,
  DETAIL_QUESTION: (id) => `/questions/${id}/`,

  // category
  CATEGORY: '/category/'
}
